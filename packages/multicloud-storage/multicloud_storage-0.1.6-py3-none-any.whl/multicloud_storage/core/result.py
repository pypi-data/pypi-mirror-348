from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class UploadResult:
    """
    UploadResult 表示一次上传操作的完整信息。
    Attributes:
      bucket   (str): 上传的存储桶名称
      key      (str): 上传时用户传入的对象键（不含 prefix）
      full_key (str): 实际存储的完整对象键（含 prefix）
      etag     (str): 对象的 ETag，用于缓存或校验
      url      (str): 公开可访问的 URL（前提是已设置公开读权限）
    """
    bucket: str     # 桶名称
    key: str        # 用户传入的 key（不含 prefix）
    full_key: str   # 实际用于存储的 full_key（含 prefix）
    etag: str       # 对象的 ETag，用于校验或缓存
    url: str        # 公开可访问的 URL（前提是服务端已设置公开读）

@dataclass
class ObjectInfo:
    """
    描述单个对象元信息
    """
    key: str               # 完整对象键（包含 prefix）
    size: int              # 大小，单位字节
    last_modified: datetime  # 最后修改时间
    etag: str              # ETag（不含双引号）

@dataclass
class ListObjectsResult:
    """
    列表操作返回值：包含本页对象列表及下一页的分页令牌
    """
    objects: List[ObjectInfo]
    next_token: Optional[str]  # 如还有后续页，则为继续请求的 token，否则 None