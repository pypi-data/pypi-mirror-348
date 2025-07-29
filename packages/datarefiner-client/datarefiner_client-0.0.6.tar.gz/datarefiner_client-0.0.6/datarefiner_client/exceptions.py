from requests import Response


class DatarefinerError(Exception):
    pass


class DatarefinerClientError(Exception):
    def __init__(self, response: Response, *args: object) -> None:
        args = (f"HTTP {response.status_code}: {response.reason}",) + args
        super().__init__(*args)


class DatarefinerClientAuthError(DatarefinerClientError):
    pass


class DatarefinerClientLockError(DatarefinerClientAuthError):
    pass


class DatarefinerClientUploadError(DatarefinerClientError):
    pass


class DatarefinerSupervisedLabelingError(DatarefinerError):
    pass


class DatarefinerExploreDownloadsError(DatarefinerError):
    pass
