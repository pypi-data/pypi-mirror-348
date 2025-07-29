from spryx_http import SpryxAsyncClient

from spryx_agents.resources.vector_stores import VectorStores


class SpryxAgents(SpryxAsyncClient):
    def __init__(
        self,
        application_id: str,
        application_secret: str,
        base_url: str = "https://agents.spryx.ai",
        iam_base_url: str = "https://iam.spryx.ai",
    ):
        super().__init__(
            base_url=base_url,
            iam_base_url=iam_base_url,
            application_id=application_id,
            application_secret=application_secret,
        )

        self.vector_stores = VectorStores(self)
