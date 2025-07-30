from abc import ABC, abstractmethod
from typing import Literal, Optional

from multicloud_storage.core.result import UploadResult, ListObjectsResult
from multicloud_storage.core.utils import normalize_endpoint

AddressingStyle = Literal['path', 'virtual']

class StorageClient(ABC):
    """
    抽象基类，定义所有 StorageClient 的公共接口和基础逻辑：
      - 规范化 endpoint、scheme、hostport
      - 保存 bucket、prefix
      - 自动检测 Content-Type（via detect_content_type）
      - 提供统一的 public_url（支持 path-style 与 virtual-hosted）
      - 定义抽象方法：upload/download/delete/presign
    """

    def __init__(self,
                 endpoint: str,
                 bucket: str,
                 prefix: str = "",
                 use_ssl: bool = True,
                 addressing_style: AddressingStyle = 'virtual',
                 public_domain: Optional[str] = None):
        """
        :param endpoint: 支持带协议和路径的 URL 字符串（后续会统一处理）
        :param bucket: 存储桶名称
        :param prefix: 对象键前缀（可为空）
        :param use_ssl: True 使用 HTTPS，False 使用 HTTP
        :param addressing_style:  'path' 或 'virtual'，决定 public_url 格式
        :param public_domain:  自定义公有读域名，public_url 会优先使用
        """
        # 规范化 endpoint → scheme, hostport
        scheme, hostport = normalize_endpoint(endpoint)
        # 保存 scheme，根据 use_ssl 强制为 http/https
        self._scheme = 'https' if use_ssl else 'http'
        self._hostport = hostport

        # 保存处理后的 endpoint
        self._endpoint = f"{self._scheme}://{self._hostport}"
        # 保存 bucket
        self._bucket = bucket
        # 统一处理 prefix（去尾斜杠）
        self._prefix = prefix.rstrip('/')

        # addressing_style 决定 public_url 的格式
        self._style = addressing_style

        # 如果构造时传了 public_domain，走 setter 做协议处理，因而这里必须是 self.public_domain 而不是 self._public_domain
        self.public_domain = public_domain

    @property
    def endpoint(self) -> str:
        """
        带协议的完整 endpoint，例如 "https://host:port"
        """
        return self._endpoint

    @property
    def bucket(self) -> str:
        """ 解析出的 bucket """
        return self._bucket

    @property
    def prefix(self) -> str:
        """ 解析出的 prefix """
        return self._prefix

    @property
    def raw_client(self):
        """
        返回底层 SDK 客户端实例，方便调用未封装的高级接口：

            client = create_storage_client(...)
            sdk = client.raw_client
            # 直接使用 sdk 的原生方法
            sdk.put_object(...)

        :return: 各子类中 self.client 所指向的对象
        """
        return getattr(self, 'client', None)

    @property
    def public_domain(self) -> Optional[str]:
        """自定义公有读域名，若不 None 则 public_url 会使用它。"""
        return self._public_domain

    @public_domain.setter
    def public_domain(self, domain: Optional[str]):
        """
        运行时可以随时设置或修改 public_domain。
        如果 domain 带协议 (http:// 或 https://)，直接使用原值；
        否则，自动加上与 endpoint 相同的协议前缀。
        """
        if not domain:
            self._public_domain = None
            return

        # 小写检测协议头
        lower = domain.lower()
        # 已包含协议前缀，就直接用
        if lower.startswith("http://") or lower.startswith("https://"):
            # 直接去掉末尾斜杠并保存
            self._public_domain = domain.rstrip('/')
        else:
            # 否则和 endpoint 使用同样的协议
            self._public_domain = f"{self._scheme}://{domain.rstrip('/')}"

    def _full_key(self, key: str) -> str:
        """
        内部方法：根据 prefix 拼接完整对象键：
          - key 前去掉左侧斜杠
          - 若 prefix 非空，则 prefix + '/' + key，否则直接 key
        """
        key = key.lstrip("/")
        return f"{self.prefix}/{key}" if self.prefix else key

    def get_full_key(self, key: str) -> str:
        """
        对外暴露的生成完整对象键的方法，等同于内部 _full_key。
        :param key: 用户传入的对象键，可能带或不带斜杠
        :return: prefix + '/' + key (若有 prefix)，否则直接 key
        """
        return self._full_key(key)

    def public_url(self, key: str) -> str:
        """
        构造公开访问 URL，

        1) 如果配置了 public_domain，返回：
            {public_domain}/{full_key}
        2) 否则根据 addressing_style 返回：
          - path:    {endpoint}/{bucket}/{full_key}
          - virtual: {scheme}://{bucket}.{hostport}/{full_key}
        :param key: 对象键（相对于 prefix）
        """
        full_key = self._full_key(key)

        # 自定义域名优先
        if self._public_domain:
            # public_domain 已含协议
            return f"{self._public_domain}/{full_key}"

        # 虚拟主机式
        if self._style == 'virtual':
            return f"{self._scheme}://{self._bucket}.{self._hostport}/{full_key}"

        # 路径式
        return f"{self._endpoint}/{self._bucket}/{full_key}"

    @abstractmethod
    def upload_file(self, local_path: str, key: str) -> UploadResult:
        """
        上传本地文件到对象存储。
        :param local_path: 本地文件绝对或相对路径
        :param key: 对象键（相对于 bucket 和 prefix）
        :return UploadResult: 包含所有信息的上传结果
        :raises UploadError: 上传失败时抛出
        """

    @abstractmethod
    def download_file(self, key: str, local_path: str) -> None:
        """
        下载对象到本地文件。
        :param key: 对象键
        :param local_path: 本地保存路径
        :raises DownloadError: 下载失败时抛出
        """

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        删除存储中的对象。
        :param key: 对象键
        :raises DeleteError: 删除失败时抛出
        """

    @abstractmethod
    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        生成对象的预签名 URL（默认 3600 秒后过期），用于临时公开访问。
        :param key: 对象键
        :param expires_in: 过期时间（秒）
        :return: 带签名的 URL 字符串
        :raises PresignError: 签名失败时抛出
        """

    @abstractmethod
    def list_objects(self,
                     prefix: str = "",
                     max_items: int = 1000,
                     next_token: Optional[str] = None,
                     sort_by: Optional[str] = None,
                     reverse: bool = False
                     ) -> ListObjectsResult:
        """
        列出指定 prefix 下的对象，统一分页和排序参数：
          :param prefix:     相对于初始化时 prefix 的子路径
          :param max_items:  本页最多返回条数
          :param next_token: 分页令牌，上一页返回的 next_token
          :param sort_by:    排序字段，可选 'key' | 'size' | 'last_modified' | 'etag'
          :param reverse:    是否倒序
          :return: ListObjectsResult(objects, next_token)
          :raises ListError: 列出对象失败时抛出
        """

    @abstractmethod
    def delete_prefix(self, prefix: str) -> None:
        """
        删除指定目录（前缀）下的所有对象。
        :param prefix: 相对于初始化时 prefix 的子路径
        :raises DeleteError: 删除过程中遇到错误时抛出
        """

    @abstractmethod
    def exists(self, key: str) -> Optional[UploadResult]:
        """
        检查指定对象是否存在：
          - 如果存在，返回对应的 UploadResult（包含 etag、url 等）
          - 如果不存在，返回 None
        :raises StorageError: 检查过程中遇到错误时抛出
        """