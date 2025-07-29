from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from datarefiner_client.utils import JupyterDataclass


@dataclass(frozen=True)
class UploadFileDetailsField(metaclass=JupyterDataclass):
    index: int
    name: str
    is_potential_id: bool
    unique_values: bool
    errors_by_type: Dict[str, Any]
    type: str
    distribution: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class UploadFileDetails(metaclass=JupyterDataclass):
    fields: List[UploadFileDetailsField]
    dataset: Dict[str, Any]
    archive_file: Optional[str]
    is_simple: Union[bool, int]
    version: float

    @property
    def fields_index_map(self) -> Dict[str, UploadFileDetailsField]:
        return {f.index: f for f in self.fields}

    @property
    def fields_name_map(self) -> Dict[str, UploadFileDetailsField]:
        return {f.name: f for f in self.fields}


@dataclass
class Upload(metaclass=JupyterDataclass):
    id: int
    title: str
    archiveFile: Optional[str] = None
    size: Optional[int] = None
    filedetails: Optional[UploadFileDetails] = None
    rows_number: Optional[int] = None
    cols_number: Optional[int] = None
