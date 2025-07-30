from typing import Any, Dict

from multicloud_storage.core.registry import get_client, get_registered_providers
from multicloud_storage.core.result import UploadResult
from multicloud_storage.core.url_parser import parse_storage_url


def create_storage_client(*,
                          provider: str = None,
                          storage_url: str = None,
                          **kwargs: Any) -> Any:
    """
    创建统一的 StorageClient 实例，支持两种方式：

    1) 通过 storage_url 初始化（带凭证和路径的完整 URL）：
       create_storage_client(
           provider='minio',
           storage_url='https://AK:SK@host/bkt/pfx'
       )

    2) 通过拆解后的参数初始化：
       create_storage_client(
           provider='minio',
           endpoint='https://minio...',
           access_key='AK',
           secret_key='SK',
           bucket='my-bucket',
           prefix='pfx',
           region='us-east-1',
           use_ssl=False
       )

    :param provider: 必填，注册时使用的名称（如 "minio","oss","s3_compatible" 或自定义扩展名）
    :param storage_url: 带凭证和路径的完整 URL
    :param kwargs: 拆解后的参数覆写（endpoint, access_key, secret_key, bucket, prefix, region, use_ssl）
    :return: StorageClient 子类实例
    :raises ValueError: provider 未指定
    """
    if not provider:
        raise ValueError("必须指定 provider")

    params: Dict[str, Any] = {}

    # 如果提供了 storage_url，则先解析
    if storage_url:
        parsed = parse_storage_url(storage_url)
        params.update(parsed)

    # 再用显式传入的 kwargs 覆盖解析结果
    params.update(kwargs)

    # 交给注册表产生实例，返回对应的客户端实例
    return get_client(provider, **params)

def get_supported_providers() -> list[str]:
    """
    获取当前已注册且可用的 provider 列表，用于展示或校验。
    """
    return get_registered_providers()

def sync_object(source_client, target_client, key: str, dest_key: str = None) -> UploadResult:
    """
    在两个存储间同步一个对象：

    从 source_client 下载 key 到临时文件，再上传到 target_client。
      1) source_client.download_file(key, temp)
      2) target_client.upload_file(temp, dest_key or key)

    :param source_client: StorageClient 源
    :param target_client: StorageClient 目标
    :param key:           源对象键
    :param dest_key:      目标对象键，若空则与 key 相同
    :return: UploadResult  目标端上传结果
    """
    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        # 下载到本地临时文件
        source_client.download_file(key, tmp.name)
        # 若没有指定目标 key ，则与源key一致
        dest = dest_key or key
        # 上传到目标并返回结果
        return target_client.upload_file(tmp.name, dest)
    finally:
        # 清理临时文件
        os.remove(tmp.name)