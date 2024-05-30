class UploadStatus:
    def __init__(self, inspectId: int, status: int, needUpload: bool, message: str | None = None):
        self.inspectId: int = inspectId
        self.status: int = status
        self.needUpload: bool = needUpload
        self.message: str | None = message

    @staticmethod
    def succeed(inspectId: int, message: str | None = None):
        return UploadStatus(inspectId, 2, False, message)

    @staticmethod
    def failure(inspectId: int, message: str | None = None):
        return UploadStatus(inspectId, 1, True, message)

    @staticmethod
    def was_uploaded(inspectId: int):
        return UploadStatus(inspectId, 3, False)

    @staticmethod
    def have_no_archive(inspectId: int):
        return UploadStatus(inspectId, 4, True)
