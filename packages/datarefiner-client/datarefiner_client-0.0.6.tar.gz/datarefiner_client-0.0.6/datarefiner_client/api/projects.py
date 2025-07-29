from time import sleep
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from requests import Session

from datarefiner_client.api.entities import Project
from datarefiner_client.api.entities.project import ProjectStatus, ProjectSteps
from datarefiner_client.iclient import IDataRefinerClient
from datarefiner_client.services.project_settings import ProjectSettings
from datarefiner_client.utils import is_notebook

if is_notebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


class ProjectsEntrypoints(IDataRefinerClient):
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs):
        self._projects_url = urljoin(self._base_url, "/api/projects")
        super(ProjectsEntrypoints, self).__init__(*args, **kwargs)

    def _make_request(self, url: str, method: str = "GET", *args: object, **kwargs: object) -> Optional[Dict[str, Any]]:
        pass

    def _create_project(self, project_settings: ProjectSettings) -> Project:
        resp = self._make_request(url=self._projects_url, method="POST", json=project_settings.to_dict())
        return Project.from_dict(resp)

    def get_project(self, project_id: int) -> Project:
        return Project.from_dict(self._make_request(url=urljoin(f"{self._projects_url}/", str(project_id))))

    def get_project_steps(self, project_id: int) -> Optional[ProjectSteps]:
        resp = self._make_request(url=urljoin(f"{self._projects_url}", f"/project/{project_id}/steps"))

        steps = resp.get("steps")
        if steps:
            return ProjectSteps.from_dict(steps)

        return None

    def create_project(self, project_settings: ProjectSettings) -> Project:
        pbar: tqdm = tqdm(total=100, desc="Create new project", unit="%", position=0, leave=False)
        project: Project = self._create_project(project_settings=project_settings)
        project_steps: ProjectSteps = self.get_project_steps(project_id=project.id)
        step_pbar_map: Dict[str, tqdm] = dict()

        pbar.set_description("Queue rendering")
        while project_steps.status in (ProjectStatus.NEW, ProjectStatus.QUEUE, ProjectStatus.RENDERING):
            sleep(1)
            project_steps = self.get_project_steps(project_id=project.id)

            if not project_steps:
                continue

            if project_steps.status is ProjectStatus.RENDERING and pbar.desc != "Rendering":
                pbar.set_description("Rendering")

            for project_progress in project_steps.steps:
                if project_progress.id not in step_pbar_map:
                    step_pbar_map[project_progress.id] = tqdm(
                        total=100, desc=project_progress.name, unit="%", position=0, leave=False
                    )
                step_pbar: tqdm = step_pbar_map[project_progress.id]

                if project_progress.status == "active":
                    step_pbar.update(n=round(project_progress.progress * 100, 2) - step_pbar.n)
                else:
                    step_pbar.update(n=step_pbar.total - step_pbar.n)
                    step_pbar.close()

            pbar.update(n=round(project_steps.progress * 100, 2) - pbar.n)

        project = self.get_project(project_id=project.id)

        if project.status in (ProjectStatus.ACTIVE, ProjectStatus.CANCELLED, ProjectStatus.ERROR):
            if project.status is ProjectStatus.CANCELLED:
                print("Rendering process canceled")
            if project.status is ProjectStatus.ERROR:
                print(project.error)
            pbar.update(n=pbar.total - pbar.n)
            pbar.close()

        return project

    def delete_project(self, project_id) -> None:
        self._make_request(url=urljoin(f"{self._projects_url}/", str(project_id)), method="DELETE")
