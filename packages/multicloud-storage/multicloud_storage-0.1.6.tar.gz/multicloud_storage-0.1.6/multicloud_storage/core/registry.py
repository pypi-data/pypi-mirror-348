"""
插件注册与工厂：通过 @register_provider 装饰器和 entry_points
自动收集各类 StorageClient 实现，并根据名称实例化。
"""

from typing import Type, Dict, Any, List

# 首先尝试使用标准库 importlib.metadata；若 Python < 3.8 则降级到 importlib_metadata
try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points

# 内部注册表：provider 名称 -> StorageClient 子类
_registry: Dict[str, Type] = {}

def register_provider(name: str):
    """
    装饰器：将 StorageClient 子类注册到 _registry。
    用法示例：
        @register_provider('minio')
        class MinioClient(StorageClient): ...
    """
    def decorator(cls: Type):
        _registry[name] = cls
        return cls
    return decorator

# —— 自动加载通过 entry_points 注册的插件 —— #
# 支持 importlib.metadata 和 importlib_metadata 两种 API
try:
    # Python 3.10+ 或新版 importlib.metadata：支持按 group 过滤
    eps = entry_points(group='multicloud_storage.providers')
except TypeError:
    # Python 3.8/3.9：entry_points() 返回一个 dict-like
    # 旧版需要过滤所有 entry_points
    eps = [ep for ep in entry_points() if ep.group == 'multicloud_storage.providers']

for ep in eps:
    # ep.name 是 provider 名称，ep.load() 会 import 对应模块并返回类
    _registry[ep.name] = ep.load()

def get_client(provider: str, **kwargs):
    """
    工厂接口：根据 provider 名称实例化并返回对应的 StorageClient。
    :param provider: 注册时用的名称（如 "minio", "oss", "s3_compatible" 或自定义插件名）
    :param kwargs: 传给该客户端 __init__ 的参数
    :return: StorageClient 子类实例
    :raises ValueError: 如果 provider 未注册
    """
    cls = _registry.get(provider)
    if not cls:
        raise ValueError(
            f"Unsupported provider '{provider}'. "
            f"已注册的 providers: {', '.join(_registry.keys())}"
        )
    return cls(**kwargs)

def get_registered_providers() -> list[str]:
    """
    返回所有已注册成功的 provider 名称列表，
    供上层展示或校验使用。
    """
    return list(_registry.keys())
