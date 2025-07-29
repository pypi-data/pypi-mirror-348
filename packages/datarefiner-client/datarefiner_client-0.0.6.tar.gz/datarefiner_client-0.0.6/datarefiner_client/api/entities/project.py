from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

import dataclasses_json
from dataclasses_json import config, dataclass_json

from datarefiner_client.utils import JupyterDataclass

dataclasses_json.cfg.global_config.encoders[datetime] = datetime.isoformat
dataclasses_json.cfg.global_config.decoders[datetime] = datetime.fromisoformat


class ProjectType(str, Enum):
    GENERIC = ""
    SUPERVISED = "supervised"
    TEXT = "text"
    TIMESERIES = "timeseries"
    IMAGES = "images"


class FieldConfigType(str, Enum):
    ID = "id"
    OVERLAY = "overlay"
    LEARN = "learn"
    DISABLE = "disable"


class FieldConfigDistributionCorrectionType(str, Enum):
    ARCSINH = "arcsinh"


class ClusterisationType(str, Enum):
    DENSE_BASED = "dense_based"
    KMEANS = "kMeans"


class DistributionCorrectionType(str, Enum):
    ON = "on"
    OFF = "off"
    AUTO = "auto"


class ModelComplexityType(str, Enum):
    TINY = "tiny"
    SMALL = "low"
    MEDIUM = "medium"
    LARGE = "high"


@dataclass
class FieldConfig(metaclass=JupyterDataclass):
    name: str
    config: FieldConfigType
    type: Optional[str] = None
    distribution_correction: Optional[FieldConfigDistributionCorrectionType] = field(
        metadata=config(exclude=lambda value: value is None), default=None
    )


@dataclass
class SupervisedParams(metaclass=JupyterDataclass):
    columns_count: int
    id_column: int
    target_column: int
    train_columns: Optional[List[int]] = field(default_factory=list)
    overlay_columns: Optional[List[int]] = field(default_factory=list)
    disabled_columns: Optional[List[int]] = field(default_factory=list)
    distribution_correction: Optional[DistributionCorrectionType] = field(default=DistributionCorrectionType.OFF)
    int_to_categorical: Optional[Union[bool, List[int]]] = field(default=False)
    target_int_to_categorical: Optional[bool] = field(default=False)
    model_complexity: Optional[ModelComplexityType] = field(default=ModelComplexityType.SMALL)


@dataclass
class ProjectJSONParams(metaclass=JupyterDataclass):
    clusterisation_type: Optional[ClusterisationType] = field(default=ClusterisationType.DENSE_BASED)
    # dense_based settings
    allow_noise_points: Optional[bool] = field(default=True)
    target_cluster_num: Optional[int] = field(default=None)
    max_cluster_num: Optional[int] = field(default=None)
    # kMeans settings
    k_means: Optional[int] = field(default=15)
    # TDA grid search settings
    metric: List[str] = field(default_factory=lambda: ["euclidean", "cosine"])
    beta: List[int] = field(default_factory=lambda: [35, 100, 200])
    # Advanced settings
    perform_normalisation: Optional[bool] = field(default=True)
    # Supervised settings
    supervised: Optional[SupervisedParams] = field(default=None)


@dataclass_json
@dataclass
class ProjectSettings(metaclass=JupyterDataclass):
    """Project settings for create and rendering new project

    Attributes:
        name (str): Project name
        upload_id (int): Upload ID of uploaded dataframe
        description (str): Project description
        project_type (ProjectType): Project type, one of ProjectType values.
            Example: ProjectType.GENERIC or ProjectType.SUPERVISED
        fields_config (Dict[str, FieldConfig]): Configuration of fields for analyzing.
            Example: {
                "0": FieldConfig(config=FieldConfigType.ID, type="int64"),
                "1": FieldConfig(config=FieldConfigType.LEARN, type="float64"),
                "2": FieldConfig(config=FieldConfigType.OVERLAY, type="float64"),
                "3": FieldConfig(config=FieldConfigType.LEARN, type="int64"),
                "4": FieldConfig(config=FieldConfigType.LEARN, type="float64")
            }
        json_params (ProjectJSONParams): Configuration of project rendering settings.
            Example: ProjectJSONParams(
                metric=["metric"],
                beta=[15],
                supervised=SupervisedParams(
                    columns_count=15,
                    id_column=0,
                    target_column=7,
                ),
            )
    """

    name: str
    upload_id: int
    description: str = field(default="")
    project_type: ProjectType = field(default=ProjectType.GENERIC, metadata=config(field_name="type"))
    fields_config: Dict[str, FieldConfig] = field(default_factory=dict)
    json_params: ProjectJSONParams = field(default_factory=ProjectJSONParams)


class ProjectStatus(str, Enum):
    NEW = "new"
    QUEUE = "queue"
    RENDERING = "rendering"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    ERROR = "error"


@dataclass_json
@dataclass(frozen=True)
class Project(metaclass=JupyterDataclass):
    id: int
    name: str
    description: str
    project_type: ProjectType = field(metadata=config(field_name="type"))
    progress: float
    status: ProjectStatus
    error: str
    created: datetime
    queued: datetime
    user_id: int
    upload_id: int
    parent_id: Optional[int]
    deep_params: Optional[str]
    profile_id: int
    json_params: ProjectJSONParams
    check_mask: int
    fields_config: Dict[str, FieldConfig]
    size: Optional[int]
    from_project_id: Optional[int]
    sliding_window: Optional[int]


@dataclass_json
@dataclass(frozen=True)
class ProjectProgress(metaclass=JupyterDataclass):
    id: str
    name: str
    status: str
    step_details: Optional[str]
    started: int
    ended: Optional[int]
    progress: float


@dataclass_json
@dataclass(frozen=True)
class ProjectSteps(metaclass=JupyterDataclass):
    progress: float
    status: ProjectStatus
    steps: List[ProjectProgress]
