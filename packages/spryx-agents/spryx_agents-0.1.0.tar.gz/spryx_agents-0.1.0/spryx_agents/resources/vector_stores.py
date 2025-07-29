from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient

from spryx_agents.types.vector_store import VectorFileStatus


class VectorStores:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def update_vector_file(
        self,
        vector_store_id: str,
        file_id: str,
        status: VectorFileStatus,
        failed_reason: str = NOT_GIVEN,
        tokens_size: int = NOT_GIVEN,
    ) -> dict:
        payload = {"status": status.value}

        if is_given(failed_reason):
            payload["failed_reason"] = failed_reason

        if is_given(tokens_size):
            payload["tokens_size"] = tokens_size

        return await self._client.put(
            f"/vector-stores/{vector_store_id}/files/{file_id}",
            json=payload,
        )
