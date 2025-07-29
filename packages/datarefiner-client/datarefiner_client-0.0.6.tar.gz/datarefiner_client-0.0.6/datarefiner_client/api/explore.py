from base64 import b64encode
from typing import Any, Dict, Optional, Union
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse, ParseResult

from IPython.display import IFrame
from requests import Session

from datarefiner_client.iclient import IDataRefinerClient


class ExploreEntrypoints(IDataRefinerClient):
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs) -> None:
        self._explore_url = urljoin(self._base_url, "/explore")
        super(ExploreEntrypoints, self).__init__(*args, **kwargs)

    def _make_request(self, url: str, method: str = "GET", *args: object, **kwargs: object) -> Optional[Dict[str, Any]]:
        pass

    def _make_project_explore_url(self, project_id: int) -> str:
        project_explore_url = urljoin(f"{self._explore_url}/", str(project_id))
        project_explore_url_parts = list(urlparse(project_explore_url))
        query_params = parse_qs(project_explore_url_parts[4])
        query_params["is_notebook"] = 1
        project_explore_url_parts[4] = urlencode(query_params)
        return urlunparse(project_explore_url_parts)

    def explore(
        self, project_id: int, width: Optional[Union[int, str]] = None, height: Optional[Union[int, str]] = None
    ) -> IFrame:
        width = width or "100%"
        height = height or 720

        project_explore_url_parts: ParseResult = urlparse(self._make_project_explore_url(project_id=project_id))

        return IFrame(
            src=urljoin(self._base_url, "/login"),
            width=width,
            height=height,
            extras=[
                'sandbox="allow-same-origin || allow-top-navigation || allow-forms || allow-scripts || allow-downloads"'
            ],
            next=f"{project_explore_url_parts.path}?{project_explore_url_parts.query}",
            is_notebook=1,
            token=b64encode(self._token.encode("utf-8")).decode("utf-8"),
        )

    def explore_rename_cluster(self, project_id: int, cluster_id: int, name: str) -> None:
        self._make_request(
            urljoin(base=f"{self._explore_url}/", url=f"{project_id}/clusters/{cluster_id}"),
            method="PUT",
            json={"name": name},
        )
