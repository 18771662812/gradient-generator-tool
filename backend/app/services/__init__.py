class ServiceError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(ServiceError):
    def __init__(self, message="资源不存在"):
        super().__init__(message, 404)


class ForbiddenError(ServiceError):
    def __init__(self, message="无权操作"):
        super().__init__(message, 403)


class ConflictError(ServiceError):
    def __init__(self, message="资源已存在"):
        super().__init__(message, 409)
