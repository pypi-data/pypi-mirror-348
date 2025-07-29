from io import BytesIO
from typing import Optional, Union, Dict, Any
from urllib.parse import urljoin

import pandas as pd
from requests import Session

from datarefiner_client.exceptions import DatarefinerExploreDownloadsError
from datarefiner_client.iclient import IDataRefinerClient


class ExploreExportsEntrypoints(IDataRefinerClient):
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs):
        self._explore_url: str = urljoin(base=self._base_url, url="/explore")
        super().__init__(*args, **kwargs)

    def _make_request(
        self, url: str, method: str = "GET", return_json: bool = True, *args: object, **kwargs: object
    ) -> Optional[Union[Dict[str, Any], bytes]]:
        pass

    def _make_df(self, url: str) -> pd.DataFrame:
        return pd.read_csv(BytesIO(self._make_request(url=url, stream=True)))

    def get_cluster_labels(self, project_id: int) -> pd.DataFrame:
        return self._make_df(url=urljoin(base=f"{self._explore_url}/", url=f"{project_id}/download/sourceids/clusters"))

    def get_group_labels(self, project_id: int) -> pd.DataFrame:
        groups = self._make_request(url=urljoin(base=f"{self._explore_url}/", url=f"{project_id}/groups"))
        if len(groups.get("groups", {}).keys()) == 0:
            raise DatarefinerExploreDownloadsError("No groups available for export")
        return self._make_df(url=urljoin(base=f"{self._explore_url}/", url=f"{project_id}/download/sourceids/groups"))

    def get_parameter_scores_for_segmentation(self, project_id: int) -> pd.DataFrame:
        return self._make_df(url=urljoin(base=f"{self._explore_url}/", url=f"{project_id}/download/topfeatures"))

    def get_most_important_features_for_all_clusters(self, project_id: int) -> pd.DataFrame:
        return self._make_df(
            url=urljoin(base=f"{self._explore_url}/", url=f"{project_id}/download/clusterstopfeatures")
        )

    def get_tda_coordinates(self, project_id: int) -> pd.DataFrame:
        return self._make_df(url=urljoin(base=f"{self._explore_url}/", url=f"{project_id}/download/tdacoordinates"))
