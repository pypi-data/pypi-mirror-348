from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from requests import Session

from datarefiner_client.api.entities import SupervisedLabel
from datarefiner_client.exceptions import DatarefinerClientError
from datarefiner_client.iclient import IDataRefinerClient


class SupervisedLabelsEntrypoints(IDataRefinerClient):
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs):
        self._supervised_labels_url = urljoin(self._base_url, "/project/{project_id}/supervised-labels")
        super(SupervisedLabelsEntrypoints, self).__init__(*args, **kwargs)

    def _make_request(self, url: str, method: str = "GET", *args: object, **kwargs: object) -> Optional[Dict[str, Any]]:
        pass

    def supervised_labels_get(self, project_id: int, supervised_label_id: int) -> SupervisedLabel:
        return (
            [
                supervised_label
                for supervised_label in self.supervised_labels_list(project_id=project_id)
                if supervised_label.id == supervised_label_id
            ]
            or (None,)
        )[0]

    def supervised_labels_get_by_upload_id(self, project_id: int, upload_id: int) -> SupervisedLabel:
        return (
            [
                supervised_label
                for supervised_label in self.supervised_labels_list(project_id=project_id)
                if supervised_label.upload_id == upload_id
            ]
            or (None,)
        )[0]

    def supervised_labels_list(self, project_id: int) -> List[SupervisedLabel]:
        with self.session.get(url=self._supervised_labels_url.format(project_id=project_id)) as resp:
            if not resp.ok:
                raise DatarefinerClientError(response=resp)
            supervised_labels, sizes = resp.json().values()
            return [
                SupervisedLabel(**dict(supervised_label, size=sizes.get(str(supervised_label["id"]))))
                for supervised_label in supervised_labels
            ]

    def supervised_labels_create(self, project_id: int, upload_id: int) -> SupervisedLabel:
        with self.session.post(
            url=self._supervised_labels_url.format(project_id=project_id), json={"upload_id": upload_id}
        ) as resp:
            if not resp.ok:
                raise DatarefinerClientError(response=resp)
            return SupervisedLabel(**dict(resp.json(), upload_id=upload_id))

    def supervised_labels_delete(self, project_id: int, supervised_label_id: int) -> None:
        with self.session.delete(
            url=urljoin(f"{self._supervised_labels_url.format(project_id=project_id)}/", str(supervised_label_id))
        ) as resp:
            if not resp.ok:
                raise DatarefinerClientError(response=resp)

    def supervised_labels_check(self, project_id: int, supervised_label_id: int) -> None:
        with self.session.get(
            url=urljoin(f"{self._supervised_labels_url.format(project_id=project_id)}/", f"{supervised_label_id}/check")
        ) as resp:
            if not resp.ok:
                raise DatarefinerClientError(response=resp)

    def supervised_labels_clusters(self, project_id: int, supervised_label_id: int) -> bytes:
        with self.session.get(
            url=urljoin(
                f"{self._supervised_labels_url.format(project_id=project_id)}/", f"{supervised_label_id}/clusters"
            )
        ) as resp:
            if not resp.ok:
                raise DatarefinerClientError(response=resp)
            return resp.content

    def supervised_labels_groups(self, project_id: int, supervised_label_id: int) -> bytes:
        with self.session.get(
            url=urljoin(
                f"{self._supervised_labels_url.format(project_id=project_id)}/", f"{supervised_label_id}/groups"
            )
        ) as resp:
            if not resp.ok:
                raise DatarefinerClientError(response=resp)
            return resp.content
