"""
定义全局通用的异常类型，供各客户端实现中统一抛出和捕获。
"""

class StorageError(Exception):
    """
    所有存储相关错误的基类。
    子类可表示上传、下载、删除等不同场景。
    """

class UploadError(StorageError):
    """上传失败时抛出的异常。"""

class DownloadError(StorageError):
    """下载失败时抛出的异常。"""

class DeleteError(StorageError):
    """删除失败时抛出的异常。"""

class PresignError(StorageError):
    """生成预签名 URL 失败时抛出的异常类型。"""

class ListError(StorageError):
    """列出对象失败时抛出。"""
    pass