from datetime import timedelta
from typing import Optional

import alibabacloud_oss_v2 as ossv2
from alibabacloud_oss_v2 import ListObjectsV2Request, HeadObjectRequest, DeleteObject, DeleteMultipleObjectsRequest
from alibabacloud_oss_v2.client import Client as V2Client
from alibabacloud_oss_v2.config import load_default as load_v2_config
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from alibabacloud_oss_v2.models import (
    PutObjectRequest, GetObjectRequest, DeleteObjectRequest
)

from multicloud_storage.core.base import StorageClient
from multicloud_storage.core.exceptions import (
    UploadError, DownloadError, DeleteError, PresignError, ListError, StorageError
)
from multicloud_storage.core.providers import OSS
from multicloud_storage.core.registry import register_provider
from multicloud_storage.core.result import UploadResult, ListObjectsResult, ObjectInfo
from multicloud_storage.core.utils import detect_content_type, extract_region, detect_service_type, \
    detect_addressing_style


@register_provider(OSS)
class OSSV2Client(StorageClient):
    """
    阿里云 OSS 客户端（v2 SDK），虚拟主机模式访问。
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
        :param endpoint: OSS Endpoint，例如 https://oss-cn-hangzhou.aliyuncs.com
        :param access_key: AccessKeyId
        :param secret_key: AccessKeySecret
        :param bucket: 存储桶名称
        :param prefix: 公共前缀
        :param region: 区域 ID，如 cn-beijing；若 None 则自动从域名提取
        :param use_ssl: True 使用 HTTPS，False 使用 HTTP
        :param public_domain: 自定义公有读域名
        """
        # OSS 用 virtual-hosted
        # 调用父类，统一处理 endpoint、bucket、prefix、use_ssl，并指定虚拟主机模式
        super().__init__(
            endpoint=endpoint,
            bucket=bucket,
            prefix=prefix,
            use_ssl=use_ssl,
            addressing_style='virtual',
            public_domain=public_domain
        )

        # 服务类型
        self._svc = detect_service_type(self.endpoint)

        # 如果未显式传 region，则尝试从 endpoint 提取
        if region is None:
            region = extract_region(self.endpoint, self._svc)

        # 决定 addressing_style 地址方案
        self._style = detect_addressing_style(self._svc)

        # 凭证提供
        creds = StaticCredentialsProvider(access_key, secret_key)
        # 加载SDK的默认配置，并设置凭证提供者
        cfg = load_v2_config()
        cfg.credentials_provider = creds
        # 设置配置中的区域信息
        cfg.region = region
        cfg.endpoint = self._endpoint
        # 使用配置好的信息创建OSS客户端
        self.client: V2Client = ossv2.Client(cfg)

    def upload_file(self, local_path: str, key: str) -> UploadResult:
        """
        上传本地文件到 OSS，并返回 UploadResult。
        流式上传：避免一次性读取整个文件到内存
        :param local_path: 本地文件路径
        :param key: 对象键（不含 bucket 与 prefix）
        :raises UploadError: 上传失败时抛出
        """
        # 自动检测 Content-Type
        content_type = detect_content_type(local_path)

        # 获取完整对象键，自动拼接 prefix
        full_key = self._full_key(key)

        try:
            # 直接传文件流，避免一次性读取整个文件到内存
            with open(local_path, "rb") as stream:
                req = PutObjectRequest(
                    bucket=self.bucket,
                    key=full_key,
                    body=stream,
                    content_type=content_type
                )
                resp = self.client.put_object(request=req)
                etag = resp.etag or ""
        except Exception as e:
            raise UploadError(f"OSS V2 上传失败: {e}") from e

        # 构造公开访问 URL，前提：该 bucket/prefix 已配置为 Public Read
        url = self.public_url(key)

        # 返回统一的 UploadResult
        return UploadResult(
            bucket=self._bucket,
            key=key,
            full_key=full_key,
            etag=etag,
            url=url
        )

    def download_file(self, key: str, local_path: str) -> None:
        """
        从 OSS 下载对象到本地。
        :param key: 对象键
        :param local_path: 本地保存路径
        :raises DownloadError: 下载失败时抛出
        """
        full_key = self._full_key(key)
        try:
            req = GetObjectRequest(bucket=self.bucket, key=full_key)
            self.client.get_object_to_file(request=req, filepath=local_path)
        except Exception as e:
            raise DownloadError(f"OSS download_file 失败: {e}") from e

    def delete(self, key: str) -> None:
        """
        删除 OSS 上的对象。
        :param key: 对象键
        :raises DeleteError: 删除失败时抛出
        """
        full_key = self._full_key(key)
        try:
            req = DeleteObjectRequest(bucket=self.bucket, key=full_key)
            self.client.delete_object(request=req)
        except Exception as e:
            raise DeleteError(f"OSS V2 删除失败: {e}") from e

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        生成一个预签名 URL，以便临时公开访问。
        :param key: 对象键
        :param expires_in: 链接过期时间（秒）
        :raises PresignError: 生成签名失败时抛出
        """
        full_key = self._full_key(key)
        try:
            # 构造 GET 请求模型
            req = GetObjectRequest(bucket=self.bucket, key=full_key)
            # 调用 presign，传入一个 timedelta
            presign_res = self.client.presign(request=req,
                                              expires=timedelta(seconds=expires_in))
            # 从结果中取 URL
            return presign_res.url
        except Exception as e:
            # 统一抛出 PresignError，供上层捕获
            raise PresignError(f"OSS V2 预签名 URL 生成失败: {e}") from e

    def list_objects(self,
                     prefix: str = "",
                     max_items: int = 1000,
                     next_token: Optional[str] = None,
                     sort_by: Optional[str] = None,
                     reverse: bool = False
                     ) -> ListObjectsResult:
        """
        列出指定 prefix 下的对象（OSS V2 SDK）。
        使用 continuation_token 分页，捕获异常为 ListError。
        """
        # 拼接完整的对象前缀
        full_prefix = self._full_key(prefix)

        try:
            # 构造 OSS V2 的 ListObjectsV2Request
            req = ListObjectsV2Request(
                bucket=self.bucket,
                prefix=full_prefix,
                max_keys=max_items,
                continuation_token=next_token
            )

            # 调用 OSS V2 SDK
            resp = self.client.list_objects_v2(request=req)
        except Exception as e:
            # 统一抛出 ListError，供上层捕获
            raise ListError(f"OSS V2 列出对象失败: {e}") from e

        # 先取 contents（可能为 None 或空列表）
        raw_contents = resp.contents or []
        # 如果没有对象，直接返回空结果
        if not raw_contents:
            return ListObjectsResult(objects=[], next_token=None)

        # 解析每个对象
        infos = [
            ObjectInfo(
                key=obj.key,
                size=obj.size,
                last_modified=obj.last_modified,
                etag=obj.etag or ""
            )
            for obj in raw_contents
        ]

        # 排序（只在有内容且指定了 sort_by 时执行）
        if sort_by:
            infos.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)

        # 获取下一页令牌
        next_token = getattr(resp, 'next_continuation_token', None)

        # 返回结果
        return ListObjectsResult(objects=infos, next_token=next_token)


    def delete_prefix(self, prefix: str) -> None:
        """
        使用 delete_multiple_objects 批量删除指定前缀下的所有对象。

        :param prefix: 相对于初始化时 prefix 的子路径
        :raises DeleteError: 删除过程遇到错误时抛出
        """
        token = None
        # 循环分页
        while True:
            # 使用统一的 list_objects 方法，复用分页和异常处理
            page = self.list_objects(prefix=prefix,
                                     max_items=1000,
                                     next_token=token,
                                     sort_by=None,
                                     reverse=False)

            # 如果本页没有对象，退出
            if not page.objects:
                break

            # 构造 DeleteObject 列表（每页最多 1000 个）
            deletes = [ DeleteObject(key=obj.key) for obj in page.objects ]

            # 执行批量删除
            req_del = DeleteMultipleObjectsRequest(
                bucket=self.bucket,
                encoding_type='url',
                objects=deletes
            )
            try:
                self.client.delete_multiple_objects(request=req_del)
            except Exception as e:
                raise DeleteError(f"OSS V2 批量删除失败: {e}") from e

            # 没有下页时退出
            token = page.next_token
            if not token:
                break

    def exists(self, key: str) -> Optional[UploadResult]:
        """
        检查对象是否存在，若存在返回 UploadResult，否则 None。
        :param key: 相对于 bucket/prefix 的对象键
        :raises StorageError: 检查时出错抛出
        """
        full_key = self._full_key(key)
        req = HeadObjectRequest(bucket=self.bucket, key=full_key)
        try:
            # head_object 不返回 body，只返回元数据
            resp = self.client.head_object(request=req)
        except Exception as e:
            # OSS 不存在时通常会抛 OssError，包含 "NoSuchKey"
            msg = str(e)
            if "NoSuchKey" in msg or "404" in msg:
                return None
            raise StorageError(f"OSSV2 exists 检查失败: {e}") from e

        # 构造 UploadResult
        etag = resp.etag or ""
        url = self.public_url(key)
        return UploadResult(
            bucket=self.bucket,
            key=key,
            full_key=full_key,
            etag=etag,
            url=url
        )
