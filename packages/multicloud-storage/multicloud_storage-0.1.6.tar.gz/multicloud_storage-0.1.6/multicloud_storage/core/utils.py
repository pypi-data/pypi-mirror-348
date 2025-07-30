import re
from typing import Optional, Literal
from urllib.parse import urlparse

# 服务类型枚举
ServiceType = Literal['oss', 'aws_s3', 's3_compatible']

"""
公共工具模块，包含：
  - endpoint 规范化
  - MIME 类型检测
  - 服务类型判断
  - region 提取
  - addressing_style 决定
"""

def normalize_endpoint(endpoint: str) -> tuple[str, str]:
    """
    将用户传入的 endpoint（可能带协议、路径）规范化为：
      scheme   = 'http' 或 'https'
      hostport = 'host:port'
    这样便于各客户端按需组合初始化 SDK。
    :param endpoint: 用户输入的 endpoint，如:
                     - "host:port"
                     - "http://host:port"
                     - "https://host:port/some/path"
    :return: tuple(scheme: str, hostport: str)
    scheme (str): 'http' 或 'https'
    hostport (str): 纯“host:port”格式，去掉任何前缀协议和路径
    """
    # 使用 urllib.parse.urlparse 解析
    parsed = urlparse(endpoint)
    # parsed.netloc 包含 host:port（若提供了协议），否则放到 parsed.path
    hostport = parsed.netloc or parsed.path
    # 去除末尾所有斜杠
    hostport = hostport.rstrip('/')
    # 解析 scheme；若无则默认 http
    scheme = parsed.scheme if parsed.scheme else 'http'
    return scheme, hostport

def detect_content_type(path: str) -> str:
    """
    自动检测文件的 MIME 类型：
      1) 优先尝试 python-magic（只读文件头部，不会加载整个大文件）
      2) fallback 到标准库 mimetypes.guess_type
      3) 最终回退到 application/octet-stream

    :param path: 文件本地路径
    :return: 合法的 content_type 字符串
    """
    # 尝试 python-magic
    try:
        import magic
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(path)
        if content_type:
            return content_type
    except ImportError:
        pass
    except Exception:
        pass

    # fallback: mimetypes
    import mimetypes
    content_type, _ = mimetypes.guess_type(path)
    return content_type or "application/octet-stream"

def detect_service_type(endpoint: str) -> ServiceType:
    """
    根据 endpoint 判断对象存储服务类型：
      - 包含 "aliyuncs.com"      → 阿里 OSS
      - 包含 "amazonaws.com"     → AWS 官方 S3
      - 其他                     → 通用 S3 兼容
    :param endpoint: 带协议的完整 endpoint
    :return: 服务类型字符串
    """
    host = urlparse(endpoint).netloc.lower()
    if 'aliyuncs.com' in host:
        return 'oss'
    if 'amazonaws.com' in host:
        return 'aws_s3'
    return 's3_compatible'

def extract_region(endpoint: str, service: ServiceType) -> Optional[str]:
    """
    从 endpoint 中提取 region：
      - 阿里 OSS: 例如 "oss-cn-beijing.aliyuncs.com" → "cn-beijing"
      - AWS S3 : 例如 "s3.cn-north-1.amazonaws.com" 或 "s3-cn-north-1.amazonaws.com" → "cn-north-1"
      - 其它兼容服务: 不处理，返回 None
    :param endpoint: 带协议的完整 endpoint
    :param service:  通过 detect_service_type 得到的服务类型
    :return: 区域 ID 或 None
    """
    host = urlparse(endpoint).netloc.split(':')[0].lower()
    if service == 'oss':
        m = re.search(r'oss-([^.]+)\.', host)
        return m.group(1) if m else None
    if service == 'aws_s3':
        m = re.search(r's3[.-]([^.]+)\.', host)
        return m.group(1) if m else None
    return None

def detect_addressing_style(service: ServiceType) -> Literal['virtual', 'path']:
    """
    根据服务类型返回推荐的 addressing_style：
      - AWS 官方 S3        → virtual-hosted（"virtual"）
      - 阿里 OSS/通用兼容 → path-style    （"path"）
    :param service: 服务类型
    :return: "virtual" 或 "path"
    """
    return 'virtual' if service == 'aws_s3' or service == 'oss' else 'path'