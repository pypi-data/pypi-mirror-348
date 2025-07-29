from io import BytesIO
from time import sleep
from typing import Any, Callable, Dict, Optional, cast, Tuple, Union
from urllib.parse import urljoin

import pandas as pd
from requests import Response, Session, codes, JSONDecodeError

from datarefiner_client.api.entities import SupervisedLabelStatus
from datarefiner_client.api.explore import ExploreEntrypoints
from datarefiner_client.api.explore_exports import ExploreExportsEntrypoints
from datarefiner_client.api.projects import ProjectsEntrypoints
from datarefiner_client.api.supervised_labels import SupervisedLabelsEntrypoints
from datarefiner_client.api.uploads import UploadsEntrypoints
from datarefiner_client.exceptions import (
    DatarefinerClientAuthError,
    DatarefinerClientError,
    DatarefinerClientLockError,
    DatarefinerSupervisedLabelingError,
)
from datarefiner_client.settings import API_BASE_URL, API_TOKEN
from datarefiner_client.utils import is_notebook

if is_notebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


def default_session_factory() -> Session:
    return Session()


class DataRefinerClient(
    ProjectsEntrypoints,
    UploadsEntrypoints,
    SupervisedLabelsEntrypoints,
    ExploreEntrypoints,
    ExploreExportsEntrypoints,
):
    _base_url: str = API_BASE_URL
    _session: Session

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
        session_factory: Optional[Callable[[], Session]] = None,
        *args,
        **kwargs,
    ):
        self._token = token or API_TOKEN
        self._base_url = base_url or self._base_url
        self._session_factory = session_factory or default_session_factory

        if self._token:
            self._set_token(token=self._token)

        super(DataRefinerClient, self).__init__(*args, **kwargs)

    @property
    def session(self) -> Session:
        if not hasattr(self, "_session"):
            self._session = self._session_factory()
        return self._session

    def _set_token(self, token: str) -> None:
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _make_request(self, url: str, method: str = "GET", *args, **kwargs) -> Optional[Union[Dict[str, Any], bytes]]:
        kwargs.setdefault("allow_redirects", False)
        with self.session.request(method=method, url=url, *args, **kwargs) as resp:
            if resp.is_redirect:
                if "/lock" in resp.headers.get("Location", ""):
                    raise DatarefinerClientLockError(
                        response=cast(
                            Response,
                            type("Response", (object,), {"status_code": codes.unauthorized, "reason": "Token locked"}),
                        )
                    )

            if not resp.ok:
                raise DatarefinerClientError(response=resp)

            if kwargs.get("stream"):
                return resp.content
            else:
                try:
                    return resp.json()
                except JSONDecodeError:
                    return resp.content

    def auth(self, email: str, password: str) -> None:
        assert email, "Email must be set"
        assert password, "Password must be set"
        with self.session.post(
            url=urljoin(self._base_url, "/api/auth"), json={"email": email, "password": password}
        ) as resp:
            if not resp.ok:
                raise DatarefinerClientAuthError(response=resp)
            data = resp.json()
        self._set_token(token=data["access_token"])

    def me(self) -> Any:
        return self._make_request(url=urljoin(self._base_url, "/api/auth"))

    def supervised_labeling(self, project_id: int, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        upload, _ = self.upload(df)

        pbar: tqdm = tqdm(desc="Check dataframe", total=100, unit="%", position=0, leave=False)
        supervised_label = self.supervised_labels_get_by_upload_id(project_id=project_id, upload_id=upload.id)
        pbar.update(n=0)
        if not supervised_label or supervised_label.status == SupervisedLabelStatus.ERROR:
            pbar.update(n=0)
            if supervised_label:
                self.supervised_labels_delete(project_id=project_id, supervised_label_id=supervised_label.id)
                pbar.update(n=0)
            supervised_label = self.supervised_labels_create(project_id=project_id, upload_id=upload.id)
            pbar.update(n=0)
        if supervised_label.status == SupervisedLabelStatus.CHECKING:
            pbar.update(n=0)
            self.supervised_labels_check(project_id=project_id, supervised_label_id=supervised_label.id)
            pbar.update(n=0)
        pbar.update(n=pbar.total - pbar.n)
        pbar.close()

        pbar: tqdm = tqdm(desc="Labeling dataframe", total=100, unit="%", position=0, leave=False)
        while (
            supervised_label := self.supervised_labels_get(
                project_id=project_id, supervised_label_id=supervised_label.id
            )
        ).status not in (SupervisedLabelStatus.COMPLETE, SupervisedLabelStatus.ERROR):
            pbar.update(n=0)
            sleep(1)
        pbar.update(n=pbar.total - pbar.n)
        pbar.close()

        if supervised_label.status == SupervisedLabelStatus.ERROR:
            raise DatarefinerSupervisedLabelingError(supervised_label.error)
        clusters_df: pd.DataFrame = pd.read_csv(
            BytesIO(self.supervised_labels_clusters(project_id=project_id, supervised_label_id=supervised_label.id))
        )
        groups_df: Optional[pd.DataFrame] = None
        if supervised_label.has_groups:
            groups_df = pd.read_csv(
                BytesIO(self.supervised_labels_groups(project_id=project_id, supervised_label_id=supervised_label.id))
            )
        return clusters_df, groups_df
