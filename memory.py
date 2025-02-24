import asyncio
import httpx
from typing import Dict, Any, Optional

class AIMemory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self.client.aclose()

    async def aget(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    async def apost(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self.client.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    # Synchronous methods
    def _run_in_thread_or_loop(self, coro):
        # Run the coroutine in the current event loop or create a new one if none exists
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(coro)  # Running within an existing event loop
        except RuntimeError:
            # No running event loop; create and run one
            asyncio.run(coro)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._run_in_thread_or_loop(self.aget(endpoint, params))

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._run_in_thread_or_loop(self.apost(endpoint, data))

    def __del__(self):
        try:
            self._run_in_thread_or_loop(self.close())
        except RuntimeError:
            # If there's no running event loop, we can't close the client
            pass