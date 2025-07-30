from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from multicloud_storage.core.base import StorageClient
from multicloud_storage.core.exceptions import UploadError, DownloadError, DeleteError, PresignError, ListError, \
    StorageError
from multicloud_storage.core.providers import S3_COMPATIBLE
from multicloud_storage.core.registry import register_provider
from multicloud_storage.core.result import UploadResult, ListObjectsResult, ObjectInfo
from multicloud_storage.core.utils import detect_content_type, detect_service_type, extract_region, \
    detect_addressing_style


@register_provider(S3_COMPATIBLE)
class S3CompatClient(StorageClient):
    """
    通用 S3 兼容客户端，根据 endpoint 自动选择：
      - service_type: OSS / AWS S3 / 兼容
      - region:       自动提取或用户指定
      - addressing_style: virtual-hosted or path-style
    """

    def __init__(self,
                 endpoint: str,
                 access_key: str,
                 secret_key: str,
                 bucket: str,
                 prefix: str = "",
                 region: Optional[str] = None,
                 use_ssl: bool = True,
                 public_domain: Optional[str] = None):
        """
        :param endpoint: S3 兼容服务地址，例如 https://s3.amazonaws.com
        :param access_key: S3 ACCESS_KEY
        :param secret_key: S3 SECRET_KEY
        :param bucket: 存储桶名称
        :param prefix: 公共前缀
        :param region: 区域 ID，例如 "us-east-1"，若不传，会尝试从 endpoint 提取
        :param use_ssl: True 使用 HTTPS，False 使用 HTTP
        :param public_domain: 自定义公有读域名
        """
        # 父类自动解析 endpoint、处理并保存 bucket/prefix/use_ssl 等
        super().__init__(
            endpoint=endpoint,
            bucket=bucket,
            prefix=prefix,
            use_ssl=use_ssl,
            public_domain=public_domain
        )

        # 服务类型
        self._svc = detect_service_type(self.endpoint)

        # 如果未显式传 region，则尝试从 endpoint 提取
        if region is None:
            region = extract_region(self.endpoint, self._svc)

        # 决定 addressing_style 地址方案
        self._style = detect_addressing_style(self._svc)

        # 设置 boto3 Config：使用 v4 签名 & addressing_style
        cfg = Config(signature_version='s3v4',
                     s3={'addressing_style': self._style})

        # 初始化 boto3 Session & 客户端
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        self.client = session.client(
            's3',
            endpoint_url=self.endpoint,
            config=cfg,
            use_ssl=use_ssl
        )

    def upload_file(self, local_path: str, key: str) -> UploadResult:
        """
        上传本地文件，并返回 UploadResult。
        内部会自动检测文件的 Content-Type。
        :param local_path: 本地文件路径
        :param key:        对象键（相对于 bucket 和 prefix）
        :raises UploadError: 上传或获取 etag 失败时抛出
        """
        # 自动检测 Content-Type
        content_type = detect_content_type(local_path)

        # 拼接完整键
        full_key = self._full_key(key)

        try:
            # 上传文件，upload_file 不返回结果
            self.client.upload_file(
                Filename=local_path,
                Bucket=self._bucket,
                Key=full_key,
                ExtraArgs={
                    'ContentType': content_type,
                }
            )
            # 额外调用 head_object 获取 etag
            head = self.client.head_object(Bucket=self._bucket, Key=full_key)
            etag = head.get('ETag', '')
        except ClientError as e:
            raise UploadError(f"S3Compat upload_file 失败: {e}") from e

        # 构造公开访问 URL，前提：该 bucket/prefix 已配置为 Public Read（公共读）
        url = self.public_url(key)

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
        :param key: 对象键
        :param local_path: 本地保存路径
        :raises DownloadError: 下载失败时抛出
        """
        full_key = self._full_key(key)
        try:
            self.client.download_file(self._bucket, full_key, local_path)
        except ClientError as e:
            raise DownloadError(f"S3Compat download_file 失败: {e}") from e

    def delete(self, key: str) -> None:
        """
        删除指定对象。
        :param key: 对象键
        :raises DeleteError: 删除失败时抛出
        """
        full_key = self._full_key(key)
        try:
            self.client.delete_object(Bucket=self._bucket, Key=full_key)
        except ClientError as e:
            raise DeleteError(f"S3Compat delete 失败: {e}") from e

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        生成临时访问 签名URL，可用于短期公开访问。
        :param key: 对象键
        :param expires_in: 链接过期时间（秒）
        :raises PresignError: 生成签名失败时抛出
        """
        full_key = self._full_key(key)
        try:
            # generate_presigned_url 方法，ClientMethod 指定 get_object
            return self.client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self._bucket, 'Key': full_key},
                ExpiresIn=expires_in
            )
        except ClientError as e:
            raise PresignError(f"S3Compat generate_presigned_url 失败: {e}") from e

    def list_objects(self,
                     prefix: str = "",
                     max_items: int = 1000,
                     next_token: Optional[str] = None,
                     sort_by: Optional[str] = None,
                     reverse: bool = False
                     ) -> ListObjectsResult:
        """
        列出指定 prefix 下的对象（S3 兼容接口）。
        使用 ContinuationToken 分页，包装异常为 ListError。
        """
        # 拼接完整的对象前缀
        full_prefix = self._full_key(prefix)

        try:
            # 构造 list_objects_v2 的参数字典
            params = {
                "Bucket": self.bucket,
                "Prefix": full_prefix,
                "MaxKeys": max_items
            }
            # 只有在翻页时才加这个字段
            if next_token:
                params["ContinuationToken"] = next_token

            resp = self.client.list_objects_v2(**params)
        except Exception as e:
            # 统一抛出 ListError，供上层捕获
            raise ListError(f"S3Compat 列出对象失败: {e}") from e

        # 解析返回的内容列表
        contents = resp.get("Contents", [])
        # 如果没有对象，直接返回空结果
        if not contents:
            return ListObjectsResult(objects=[], next_token=None)

        # 解析每个对象
        infos = [
            ObjectInfo(
                key=item["Key"],
                size=item["Size"],
                last_modified=item["LastModified"],
                etag=item["ETag"].strip('"')
            )
            for item in contents
        ]

        # 本地排序（如果需要）
        if sort_by:
            infos.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)

        # 拿到下一页的 token
        next_token = resp.get("NextContinuationToken")

        # 返回结果
        return ListObjectsResult(objects=infos, next_token=next_token)


    def delete_prefix(self, prefix: str) -> None:
        """
        删除指定目录（前缀）下的所有对象。
        :param prefix: 相对于初始化时 prefix 的子路径
        :raises DeleteError: 删除失败时抛出
        """
        token = None
        # 循环分页删除
        while True:
            page = self.list_objects(prefix=prefix,
                                     max_items=1000,
                                     next_token=token)
            # 空页结束
            if not page.objects:
                break

            # 对本页中的每个对象，调用单对象删除接口
            for obj in page.objects:
                try:
                    self.client.delete_object(
                        Bucket=self.bucket,
                        Key=obj.key
                    )
                except ClientError as e:
                    # 捕获并包装为统一的 DeleteError
                    raise DeleteError(f"S3Compat 删除 `{obj.key}` 失败: {e}") from e

            # # 批量删除（Boto3 delete_objects）（注意：这里不使用批量删除，因为 boto3 调用 delete_objects 时，新版本不再支持自动填充Content-Md5，导致报错 Missing required header for this request: Content-Md5.）
            # keys = [{'Key': obj.key} for obj in page.objects]
            # try:
            #     self.client.delete_objects(
            #         Bucket=self.bucket,
            #         Delete={'Objects': keys}
            #     )
            # except ClientError as e:
            #     raise DeleteError(f"S3Compat 批量删除失败: {e}") from e

            # 下一页
            token = page.next_token
            if not token:
                break

    def exists(self, key: str) -> Optional[UploadResult]:
        """
        检查对象是否存在，并返回 UploadResult。
        :param key: 相对于 bucket/prefix 的对象键
        :return: 若存在则 UploadResult，否则 None
        :raises StorageError: 其它错误抛出
        """
        full_key = self._full_key(key)
        try:
            # head_object 不下载内容，只获取元数据
            resp = self.client.head_object(
                Bucket=self.bucket,
                Key=full_key
            )
        except ClientError as e:
            code = e.response.get('Error', {}).get('Code', '')
            # 404/NotFound/NoSuchKey 表示不存在
            if code in ('404', 'NotFound', 'NoSuchKey'):
                return None
            # 其它错误视为异常
            raise StorageError(f"S3Compat exists 检查时发生错误: {e}") from e

        # 构造并返回 UploadResult
        etag = resp.get('ETag', '').strip('"')
        url = self.public_url(key)
        return UploadResult(
            bucket=self.bucket,
            key=key,
            full_key=full_key,
            etag=etag,
            url=url
        )
