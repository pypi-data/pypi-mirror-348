from urllib.parse import urlparse, unquote
from typing import Dict

def parse_storage_url(storage_url: str) -> Dict[str, str]:
    """
    将 Oxylabs 风格的 storage_url:
      https://ACCESS:SECRET@host[:port]/bucket[/prefix...]
    解析为 create_storage_client 所需的参数：
    返回字典，包含：
      - endpoint (str): 带 scheme 的主机地址
      - access_key (str)
      - secret_key (str)
      - bucket (str)
      - prefix (str)
      - use_ssl (bool)

    :param storage_url: 带凭证和路径的完整 URL
    :return: 参数字典
    :raises ValueError: 若缺少用户名或密码
    """
    parsed = urlparse(storage_url)
    # 校验协议
    if not parsed.scheme:
        raise ValueError(
            f"storage_url 缺少协议（http:// 或 https://），当前值: '{storage_url}'"
        )

    # 校验 ACCESS_KEY
    if not parsed.username:
        raise ValueError(
            f"storage_url 缺少 ACCESS_KEY，正确示例: "
            f"'scheme://ACCESS:SECRET@host:port/bucket', 当前值: '{storage_url}'"
        )

    # 校验 SECRET_KEY
    if not parsed.password:
        raise ValueError(
            f"storage_url 缺少 SECRET_KEY，正确示例: "
            f"'scheme://ACCESS:SECRET@host:port/bucket', 当前值: '{storage_url}'"
        )

    # 校验主机名
    if not parsed.hostname:
        raise ValueError(
            f"storage_url 缺少主机名（host），正确示例: "
            f"'scheme://ACCESS:SECRET@host:port/bucket', 当前值: '{storage_url}'"
        )

    # 校验 path，必须至少包含 bucket
    path = parsed.path.lstrip("/")
    if not path:
        raise ValueError(
            f"storage_url path 部分必须包含 bucket 名称，正确示例: "
            f"'scheme://ACCESS:SECRET@host:port/bucket', 当前值: '{storage_url}'"
        )

    # 解码 ACCESS/SECRET（可能包含 URL 转义）
    access_key = unquote(parsed.username)
    secret_key = unquote(parsed.password)

    # 构造带协议的 endpoint，例如 "http(s)://host:port"
    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port
    endpoint = f"{scheme}://{host}"
    if port:
        endpoint += f":{port}"

    # 根据 scheme 自动设置 use_ssl
    use_ssl = scheme == "https"

    # 解析 path 部分，去掉最左斜杠后按 '/' 分割
    # 分割出 bucket 和 可选 prefix
    parts = parsed.path.lstrip("/").split("/", 1)
    bucket = parts[0]                                       # 第一个元素是桶名
    prefix = parts[1].rstrip("/") if len(parts) > 1 else "" # 余下是 prefix

    return {
        "endpoint": endpoint,
        "access_key": access_key,
        "secret_key": secret_key,
        "bucket": bucket,
        "prefix": prefix,
        "use_ssl": use_ssl,
    }
