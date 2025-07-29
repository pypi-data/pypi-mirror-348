from typing import Any, Literal
from uuid import UUID

from qcogclient import store
from qcogclient.httpclient import HttpClient, init_client


class ProjectClient:
    _project_id: str | None = None

    def __init__(
        self,
        http_client: HttpClient | None = None,
    ) -> None:
        api_key = self.api_key

        if not api_key and not http_client:
            raise ValueError("No API key found. Login first.")

        self.client = http_client or init_client(api_key=api_key)
        self._dataset_id: str | None = None

    @property
    def dataset_id(self) -> UUID:
        if not (attr := getattr(self, "_dataset_id", None)):
            raise ValueError("No dataset ID found. Get a dataset first.")
        return UUID(attr)

    @property
    def api_key(self) -> str | None:
        """Retrieve the API key from the store"""
        partial_store = store.get({"api_key": store.GET})
        return partial_store.get("api_key", None)

    async def whoami(self) -> dict[str, Any]:
        """Returns the current user."""
        return await self.client.exec("/whoami", "GET")

    async def project_id(self) -> str:
        if not hasattr(self, "_project_id") or not self._project_id:
            whoami = await self.whoami()
            if error := whoami.get("error"):
                raise ValueError(error)
            self._project_id = whoami["response"]["project_id"]
        return str(self._project_id)

    async def create_dataset(
        self,
        *,
        name: str,
        dataset_location: str,
        credentials: dict[str, Any],
        dataset_format: Literal["csv"] = "csv",
        provider: Literal["modal"] = "modal",
        version: str = "0.0.1",
    ) -> dict[str, Any]:
        """Create a dataset.

        Parameters
        ----------
        name : str
            The name of the dataset to create.
        dataset_location : str
            The location of the dataset to create.
        credentials : dict[str, Any]
            The credentials of the dataset to create.
        dataset_format : Literal["csv"]
            The format of the dataset to create.
        provider : Literal["modal"]
            The provider of the dataset to create.
        version : str
            The version of the dataset to create.

        Returns
        -------
        dict[str, Any]
            The dataset that was created in the `response` field.
            An error in the `error` field if the dataset was not created.
        """
        project_id = await self.project_id()
        response = await self.client.exec(
            f"/projects/{project_id}/datasets",
            "POST",
            {
                "name": name,
                "configuration": {
                    "provider": provider,
                    "version": version,
                    "dataset_location": dataset_location,
                    "dataset_format": dataset_format,
                    "credentials": credentials,
                },
            },
        )

        return response

    async def list_datasets(
        self,
        *,
        limit: int = 100,
        skip: int = 0,
    ) -> dict[str, Any]:
        """List all datasets."""
        project_id = await self.project_id()
        return await self.client.exec(
            f"/projects/{project_id}/datasets", "GET", {"limit": limit, "skip": skip}
        )

    async def get_dataset(
        self,
        *,
        dataset_id: str,
        identifier: Literal["id", "name"] = "id",
        load: bool = False,
    ) -> dict[str, Any]:
        """Get a dataset by ID or name.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset to get.
        identifier : Literal["id", "name"]
            The identifier of the dataset to get.
        load : bool
            Whether to load the dataset in memory.

        Returns
        -------
        dict[str, Any]
            The dataset that was retrieved in the `response` field.
            An error in the `error` field if the dataset was not retrieved.
        """
        project_id = await self.project_id()
        result = await self.client.exec(
            f"/projects/{project_id}/datasets/{dataset_id}",
            "GET",
            params={"identifier": identifier},
        )

        if load:
            if result.get("response"):
                self._dataset_id = result["response"]["id"]

        return result
