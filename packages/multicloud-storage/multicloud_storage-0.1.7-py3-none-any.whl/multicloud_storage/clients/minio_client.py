from datetime import timedelta
from typing import Optional

from minio import Minio, S3Error
from minio.deleteobjects import DeleteObject

from multicloud_storage.core.base import StorageClient
from multicloud_storage.core.exceptions import UploadError, DownloadError, DeleteError, PresignError, ListError
from multicloud_storage.core.providers import MINIO
from multicloud_storage.core.registry import register_provider
from multicloud_storage.core.result import UploadResult, ListObjectsResult, ObjectInfo
from multicloud_storage.core.utils import detect_content_type


@register_provider(MINIO)
class MinioClient(StorageClient):
    """
    MinIO 客户端，兼容 AWS S3 协议。
    依赖：minio SDK
    """

    def __init__(self,
                 endpoint: str,
                 access_key: str,
                 secret_key: str,
                 bucket: str,
                 prefix: str = "",
                 use_ssl: bool = True,
                 public_domain: Optional[str] = None):
        """
        :param endpoint: MinIO 服务地址，例如 https://minio.example.com
        :param access_key: ACCESS_KEY
        :param secret_key: SECRET_KEY
        :param bucket: 存储桶名称
        :param prefix: 公共前缀（路径）
        :param use_ssl: 是否使用 HTTPS
        :param public_domain: 自定义公有读域名
        """
        # 调用父类构造，自动处理 endpoint、bucket、prefix、scheme
        # MinIO 建议 path-style
        super().__init__(
            endpoint=endpoint,
            bucket=bucket,
            prefix=prefix,
            use_ssl=use_ssl,
            addressing_style='path',
            public_domain=public_domain
        )

        # 用规范后的 hostport 和 use_ssl 初始化 Minio SDK
        self.client = Minio(
            endpoint=self._hostport, # 只需 host:port
            access_key=access_key,
            secret_key=secret_key,
            secure=use_ssl
        )

    def upload_file(self, local_path: str, key: str) -> UploadResult:
        """
        上传文件并返回 UploadResult。
        :raises UploadError: 上传失败时抛出
        """
        # 自动检测 Content-Type
        content_type = detect_content_type(local_path)

        # 得到带 prefix 的完整键
        full_key = self._full_key(key)

        try:
            # fput_object 返回 ObjectWriteResult，需要取 .etag
            result = self.client.fput_object(
                bucket_name=self._bucket,
                object_name=full_key,
                file_path=local_path,
                content_type=content_type,
            )
            etag = result.etag  # ObjectWriteResult.etag 返回 str
        except S3Error as e:
            # 捕获 SDK 异常并抛统一的 UploadError
            raise UploadError(f"MinIO upload_file 失败: {e}") from e

        # 利用父类实现的 public_url 构造公开 URL（前提：桶或对象已设置公开读）
        url = self.public_url(key)

        # 构造并返回 上传结果
        return UploadResult(
            bucket=self._bucket,
            key=key,
            full_key=full_key,
            etag=etag,
            url=url
        )

    def download_file(self, key: str, local_path: str) -> None:
        """
        下载对象到本地文件。
        :raises DownloadError: 失败时抛出
        """
        full_key = self._full_key(key)
        try:
            self.client.fget_object(self._bucket, full_key, local_path)
        except S3Error as e:
            raise DownloadError(f"MinIO download_file 失败: {e}") from e

    def delete(self, key: str) -> None:
        """
        删除指定对象。
        :raises DeleteError: 失败时抛出
        """
        full_key = self._full_key(key)
        try:
            self.client.remove_object(self._bucket, full_key)
        except S3Error as e:
            raise DeleteError(f"MinIO delete 失败: {e}") from e

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        生成一个带签名的临时 URL（预签名 GET URL），expires_in 单位秒。
        :raises PresignError: 生成签名失败时抛出
        """
        full_key = self._full_key(key)
        try:
            # expires_in 以秒为单位，底层 SDK 需要 timedelta。
            # 将秒数转换为 datetime.timedelta
            expires = timedelta(seconds=expires_in)

            return self.client.presigned_get_object(
                bucket_name=self._bucket,
                object_name=full_key,
                expires=expires
            )
        except S3Error as e:
            raise PresignError(f"MinIO generate_presigned_url 失败: {e}") from e

    def list_objects(self,
                     prefix: str = "",
                     max_items: int = 1000,
                     next_token: Optional[str] = None,
                     sort_by: Optional[str] = None,
                     reverse: bool = False
                     ) -> ListObjectsResult:
        """
        列出指定 prefix 下的对象（MinIO 接口）。
        使用 start_after 代替 marker，捕获 S3Error 并包装为 ListError。
        """
        # 拼接完整的对象前缀
        full_prefix = self._full_key(prefix)

        infos = []
        try:
            # start_after 支持分页
            for obj in self.client.list_objects(
                    bucket_name=self.bucket,
                    prefix=full_prefix,
                    recursive=True,
                    start_after=next_token or ""
            ):
                infos.append(ObjectInfo(
                    key=obj.object_name,
                    size=obj.size,
                    last_modified=obj.last_modified,
                    etag=obj.etag
                ))
                if len(infos) >= max_items:
                    break
        except S3Error as e:
            # 统一抛出 ListError，供上层捕获
            raise ListError(f"MinIO 列出对象失败: {e}") from e

        # 下一页标记：本页最后一项的 key，否则 None
        next_token = infos[-1].key if len(infos) >= max_items else None

        # 本地排序
        if sort_by:
            infos.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)

        return ListObjectsResult(objects=infos, next_token=next_token)

    def delete_prefix(self, prefix: str) -> None:
        """
        删除指定前缀下的所有对象。
        :param prefix: 相对于初始化时 prefix 的子路径
        :raises DeleteError: 删除失败时抛出
        """
        # 分页列出所有对象
        token = None
        while True:
            page = self.list_objects(prefix=prefix,
                                     max_items=1000,
                                     next_token=token)
            # 若结果为空，结束
            if not page.objects:
                break

            # 将本页所有对象封装为 DeleteObject 列表
            delete_list = [
                DeleteObject(obj.key) for obj in page.objects
            ]
            try:
                # 执行批量删除，返回一个错误迭代器
                errors = self.client.remove_objects(
                    bucket_name=self.bucket,
                    delete_object_list=delete_list,
                    bypass_governance_mode=False # 治理模式（Governance Mode）：bypass_governance_mode=False 为默认值，表示不跳过治理模式验证；若需绕过，可设为 True
                )  # :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}
            except S3Error as e:
                # 捕获总体调用错误并抛出
                raise DeleteError(f"MinIO 批量删除失败: {e}") from e

            # 遍历可能的单条删除失败项并收集
            err_msgs = []
            for err in errors:
                # err.name, err.code, err.message
                err_msgs.append(f"{err.name}: {err.code} / {err.message}")
            if err_msgs:
                # 如果有失败，抛出包含所有失败信息的异常
                raise DeleteError(
                    f"MinIO delete_prefix 中以下对象删除失败:\n" +
                    "\n".join(err_msgs)
                )

            # 如果无下一页，结束
            token = page.next_token
            if not token:
                break

    def exists(self, key: str) -> Optional[UploadResult]:
        """
        检查指定对象是否存在，并返回 UploadResult。
        :param key: 相对于 bucket/prefix 的对象键
        :return: 若存在则 UploadResult，否则 None
        :raises StorageError: 其它错误抛出
        """
        # 拼完整 key
        full_key = self._full_key(key)
        try:
            # StatObject 返回元信息
            info = self.client.stat_object(self.bucket, full_key)
        except S3Error as e:
            # 对象不存在时，code 是 'NoSuchKey'
            if e.code == "NoSuchKey":
                return None
            raise  # 其它错误继续抛

        # 构造 UploadResult 并返回
        etag = info.etag
        url = self.public_url(key)
        return UploadResult(
            bucket=self.bucket,
            key=key,
            full_key=full_key,
            etag=etag,
            url=url
        )
