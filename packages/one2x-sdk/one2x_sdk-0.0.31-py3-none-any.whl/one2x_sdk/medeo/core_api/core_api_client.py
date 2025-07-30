import os
import requests
import aiohttp
from one2x_sdk.utils.logger import get_default_logger


class CoreApiClient:
    def __init__(self, base_url=None, token=None, enable_requests=None, logger=None):
        self.base_url = base_url or os.getenv(
            "MEDEO_CORE_API_BASE_URL", "http://localhost:3000"
        )
        self.token = token or os.getenv("MEDEO_CORE_API_AUTH_TOKEN", "default-token")
        self.enable_requests = (
            enable_requests
            if enable_requests is not None
            else os.getenv("MEDEO_CORE_API_ENABLE_REQUESTS", "false").lower() in "true"
        )

        self.logger = logger or get_default_logger("CoreApiClient")
        self.session = requests.Session()
        self._async_session = None

    def _build_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"medeo-service-auth-token={self.token}",
        }
        return headers

    def request(self, method, api_path, params=None, data=None, json=None):
        if not self.enable_requests:
            self.logger.info(
                f"Skipping request to {api_path} in non-production environment"
            )
            return None

        url = f"{self.base_url}/{api_path.strip('/')}"
        headers = self._build_headers()

        result = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=10,
        )

        if result.status_code in [429, 502]:
            error_msg = {429: "Rate limit exceeded", 502: "Bad Gateway error"}[
                result.status_code
            ]
            self.logger.warning(f"{error_msg} for {url}")
            return None

        result.raise_for_status()

        if not result.text.strip():
            return None
        return result.json()

    async def request_async(self, method, api_path, params=None, data=None, json=None):
        """Async version of request method using aiohttp."""
        if not self.enable_requests:
            self.logger.info(
                f"Skipping request to {api_path} in non-production environment"
            )
            return None

        url = f"{self.base_url}/{api_path.strip('/')}"
        headers = self._build_headers()

        # Create async session if it doesn't exist
        if self._async_session is None:
            self._async_session = aiohttp.ClientSession()

        try:
            async with self._async_session.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=10,
            ) as response:
                if response.status in [429, 502]:
                    error_msg = {429: "Rate limit exceeded", 502: "Bad Gateway error"}[
                        response.status
                    ]
                    self.logger.warning(f"{error_msg} for {url}")
                    return None

                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "").lower()
                if "application/json" in content_type:
                    # 内容类型是JSON，直接用json方法解析
                    result = await response.json()
                    return result
                else:
                    # 非JSON内容类型，以文本处理
                    text = await response.text()
                    if not text.strip():
                        return None

                    # 处理特殊情况-布尔值字符串
                    if text.lower() == "true":
                        return True
                    if text.lower() == "false":
                        return False

                    # 尝试手动解析JSON，以防Content-Type错误设置
                    try:
                        import json

                        return json.loads(text)
                    except ValueError:
                        # 如果不是有效JSON，返回原始文本
                        return text

        except aiohttp.ClientResponseError as e:
            self.logger.error(f"Error in async request to {url}: {e}")
            raise
        except aiohttp.ClientError as e:
            self.logger.error(f"Connection error in async request to {url}: {e}")

    async def close_async_session(self):
        """Close the async session to properly release resources."""
        if self._async_session is not None:
            await self._async_session.close()
            self._async_session = None
