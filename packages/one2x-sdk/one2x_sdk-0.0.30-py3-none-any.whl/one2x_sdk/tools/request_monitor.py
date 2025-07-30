import datetime
import os
from threading import Lock

import requests

from one2x_sdk.utils.logger import get_default_logger


class RequestMonitor:
    def __init__(self, env="dev", analysis_url=None, service_name="director", project_name="medeo", enabled=True,
                 logger=None, local_logs_max_size=10):
        self.env = env or os.getenv(
            "ENV", "dev"
        )
        self.enabled = enabled
        self.analysis_url = analysis_url or os.getenv(
            "ANALYSIS_SERVICE_URL", "http://localhost:3268"
        )
        self.service_name = service_name
        self.project_name = project_name
        self.logger = logger or get_default_logger('RequestMonitor')
        self._pre_request_logs_lock = Lock()
        self._pre_request_logs = []
        self._local_logs_max_size = local_logs_max_size
        if enabled:
            self.configure()

    def configure(self):
        self._patch_aiohttp()

    def _pre_process_external_request(self, url, method=None, headers=None, data=None):
        url_str = str(url)
        if self.analysis_url and self.analysis_url in url_str:
            self.logger.debug(f"跳过监控分析服务请求: {url_str}")
            return
        if "supabase" in url_str.lower():
            self.logger.debug(f"跳过监控 supabase 请求: {url_str}")
            return
        if "one2x" in url_str.lower():
            self.logger.debug(f"跳过监控 one2x 请求: {url_str}")
            return

        if not self.enabled:
            return

        self.logger.debug(
            f"RequestMonitor Pre-process Request: {method} {url_str} {headers} {data} {self.service_name} {self.project_name} {self.env}")

        log_entry = {
            "request_time": datetime.datetime.now().isoformat(),
            "request_url": url_str,
            "request_method": method,
            "request_headers": headers,
            "request_body": data,
            "service_name": self.service_name,
            "project_name": self.project_name,
            "environment": self.env
        }

        with self._pre_request_logs_lock:
            self._pre_request_logs.append(log_entry)
            logs_to_send = None
            if len(self._pre_request_logs) >= self._local_logs_max_size and self.analysis_url:
                logs_to_send = self._pre_request_logs.copy()
                self._pre_request_logs = []
        
        # 在锁外执行网络请求
        if logs_to_send:
            try:
                requests.post(f"{self.analysis_url}/api/logs/bulk-create", json=logs_to_send,
                              timeout=5)
            except Exception as e:
                self.logger.warning(f"Failed to send request logs for analysis: {e}")

    def _post_process_external_request(self):
        pass

    def _patch_aiohttp(self):
        try:
            import aiohttp
            original_request = aiohttp.ClientSession._request

            async def patched_request(self_session, method, url, **kwargs):
                if not self.enabled:
                    return await original_request(self_session, method, url, **kwargs)

                headers = kwargs.get('headers', {})
                data = kwargs.get('data', kwargs.get('json', {}))

                self._pre_process_external_request(
                    url=url,
                    method=method,
                    headers=headers,
                    data=data
                )

                response = await original_request(self_session, method, url, **kwargs)
                self._post_process_external_request()
                return response

            aiohttp.ClientSession._request = patched_request
            self.logger.info("RequestMonitor 已对 aiohttp 库进行 AOP 拦截!")
        except ImportError:
            self.logger.info("未找到 aiohttp 库，跳过拦截")
