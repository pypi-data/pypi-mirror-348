import os
from time import sleep
from typing import IO, Any, Dict, Optional
from urllib.parse import urljoin
from uuid import uuid4

import pandas as pd
from dacite import from_dict
from requests import Session

from datarefiner_client.api.entities import Upload, UploadFileDetails
from datarefiner_client.dataframe_uploader import DataFrameUploader
from datarefiner_client.exceptions import DatarefinerClientUploadError
from datarefiner_client.iclient import IDataRefinerClient
from datarefiner_client.services.project_settings import ProjectSettings, ProjectSettingsFactory
from datarefiner_client.utils import is_notebook

if is_notebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


class UploadsEntrypoints(IDataRefinerClient):
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs):
        self._uploads_url = urljoin(self._base_url, "/upload")
        super(UploadsEntrypoints, self).__init__(*args, **kwargs)

    def _make_request(self, url: str, method: str = "GET", *args, **kwargs) -> Optional[Dict[str, Any]]:
        pass

    def _upload(self, _io: IO, title: Optional[str] = None) -> Upload:
        """
        Upload IO to Datarefiner server
        :param _io: File or Reader
        :return: Information about uploaded file on datarefiner server
        """
        filename = f"{os.path.splitext(title or str(uuid4()))[0]}.csv"
        with self.session.post(url=self._uploads_url, files={"file": (filename, _io)}) as resp:
            if not resp.ok:
                raise DatarefinerClientUploadError(response=resp)
            upload_dict = resp.json()["upload"]
            upload_dict["rows_number"] = upload_dict.pop("rows") if "cols" in upload_dict else None
            upload_dict["cols_number"] = upload_dict.pop("cols") if "cols" in upload_dict else None
            return Upload(**upload_dict)

    def _get_upload_filedetails(self, upload_id: int, pbar: Optional[tqdm] = None) -> UploadFileDetails:
        upload_api_url: str = urljoin(self._base_url, f"/api/uploads/{upload_id}/")
        file_details: Optional[Dict[str, Any]] = self._make_request(url=urljoin(upload_api_url, "details"))
        while not file_details:
            result = self._make_request(url=urljoin(upload_api_url, "progress"))
            if "report" in result:
                file_details = result["report"]
            elif "progress" in result:
                if pbar is not None:
                    pbar.update(n=round(float(result["progress"]) * 100) - pbar.n)
                    sleep(1)
            else:
                raise Exception("Unhandled result")

        if pbar is not None:
            pbar.update(n=pbar.total - pbar.n)

        return from_dict(UploadFileDetails, file_details)

    def _get_upload(self, upload_id: int) -> Upload:
        upload_api_url: str = urljoin(self._base_url, f"/api/uploads/{upload_id}")
        resp = self._make_request(url=upload_api_url)
        return from_dict(Upload, resp)

    def upload(
        self, df: pd.DataFrame, title: Optional[str] = None, load_filedetails: bool = False
    ) -> (Upload, ProjectSettings):
        # Upload pandas DataFrame
        df_io = DataFrameUploader(df)

        pbar: tqdm = tqdm(desc="Upload dataframe", total=len(df_io), unit="b", position=0, leave=False)
        df_io.set_callback(cb=lambda size: pbar.update(pbar.n + size))

        upload = self._upload(_io=df_io, title=title)
        pbar.update(n=pbar.total - pbar.n)
        pbar.close()

        # Waiting upload file details
        if load_filedetails and upload.filedetails is None:
            pbar: tqdm = tqdm(desc="Waiting upload file details", total=100, unit="%", position=0, leave=False)
            filedetails = self._get_upload_filedetails(upload_id=upload.id, pbar=pbar)
            upload = self._get_upload(upload_id=upload.id)
            upload.filedetails = filedetails
            pbar.update(n=pbar.total - pbar.n)
            pbar.close()

        return (
            upload,
            ProjectSettingsFactory.make_project_settings(upload=upload) if upload.filedetails is not None else None,
        )
