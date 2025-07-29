import os
import re
from typing import Dict, Optional, Tuple

from datarefiner_client.api.entities import (
    FieldConfig,
    FieldConfigType,
    ProjectJSONParams,
    ProjectSettings,
    ProjectType,
    SupervisedParams,
    Upload,
    UploadFileDetailsField,
)

project_name_re = re.compile(r"[^a-zA-Z0-9]+")


class ProjectSettingsFactory:
    @classmethod
    def make_project_settings(cls, upload: Upload, project_type: Optional[ProjectType] = None) -> ProjectSettings:
        """Method for make project settings from upload and project type

        :param upload: Upload of uploaded dataframe
        :param project_type: Project type for created project
        :return: Setting for create new project over API client
        """
        project_type: ProjectType = project_type or (
            ProjectType.SUPERVISED if upload.cols_number > 1000 else ProjectType.GENERIC
        )
        fields_config: Dict[str, FieldConfig] = dict()
        json_params: ProjectJSONParams = ProjectJSONParams()

        if project_type is ProjectType.GENERIC:
            id_field_idx: Optional[int] = None
            for field_ in upload.filedetails.fields:
                field_idx, a_id, field_config = cls.make_field_config(project_type=project_type, field_=field_)
                if a_id and id_field_idx is None:
                    fields_config[str(field_idx)] = FieldConfig(
                        name=field_.name, config=FieldConfigType.ID, type=field_.type
                    )
                    id_field_idx = field_idx
                    continue
                fields_config[str(field_idx)] = field_config
        elif project_type is ProjectType.SUPERVISED:
            id_field_idx: Optional[int] = None
            target_field_idx: Optional[int] = None
            for field_ in upload.filedetails.fields:
                if id_field_idx is not None and target_field_idx is not None:
                    break
                field_idx, a_id, field_config = cls.make_field_config(project_type=project_type, field_=field_)
                if a_id and id_field_idx is None:
                    id_field_idx = field_idx
                elif field_config.config is FieldConfigType.LEARN and target_field_idx is None:
                    target_field_idx = field_idx

            json_params.supervised = SupervisedParams(
                columns_count=min(50, upload.cols_number), id_column=id_field_idx, target_column=target_field_idx
            )

        project_settings: ProjectSettings = ProjectSettings(
            name=project_name_re.sub(" ", os.path.splitext(upload.title)[0]),
            upload_id=upload.id,
            project_type=project_type,
            fields_config=fields_config,
            json_params=json_params,
        )
        return project_settings

    @classmethod
    def make_field_config(
        cls, project_type: ProjectType, field_: UploadFileDetailsField
    ) -> Tuple[int, bool, FieldConfig]:
        if project_type is ProjectType.IMAGES and field_.type == "image":
            return (
                field_.index,
                False,
                FieldConfig(name=field_.name, config=FieldConfigType.LEARN, type=field_.type),
            )

        a_id, a_overlay, a_learn, a_disable = field_.unique_values, True, True, True

        if project_type is ProjectType.IMAGES:
            a_learn = False

        if field_.type == "text":
            a_overlay = False
            if project_type is not ProjectType.TEXT:
                a_learn = False

        blocked_types: Dict[str, bool] = {}
        errors_types: Dict[str, bool] = {}
        warnings_types: Dict[str, bool] = {}
        for type_, errors in field_.errors_by_type.items():
            blocked_types[type_] = len(errors.get("blocked", [])) > 0
            errors_types[type_] = len(errors.get("errors", [])) > 0
            warnings_types[type_] = len(errors.get("warnings", [])) > 0

        if blocked_types[field_.type]:
            a_overlay = False
            a_learn = False

        if errors_types[field_.type]:
            a_learn = False

        config: FieldConfigType = FieldConfigType.DISABLE
        if a_learn and not warnings_types[field_.type]:
            config = FieldConfigType.LEARN
        elif a_overlay:
            config = FieldConfigType.OVERLAY

        return field_.index, a_id, FieldConfig(name=field_.name, config=config, type=field_.type)
