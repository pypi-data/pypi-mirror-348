from bayesline.api.equity import AsyncDatasetApi, DatasetApi

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient


class AsyncDatasetClientImpl(AsyncDatasetApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("dataset")

    async def get_default_dataset_name(self) -> str:
        response = await self._client.get("", params={"type": "default"})
        response.raise_for_status()
        return response.json()[0]

    async def get_dataset_names(self) -> list[str]:
        return (await self._client.get("")).json()


class DatasetClientImpl(DatasetApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("dataset")

    def get_default_dataset_name(self) -> str:
        return self._client.get("", params={"type": "default"}).json()[0]

    def get_dataset_names(self) -> list[str]:
        return self._client.get("").json()
