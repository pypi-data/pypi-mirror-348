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
# 保存 entry_point 对象列表，第一次延迟加载时填充
_entry_points = None  # type: ignore

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

def _load_providers() -> None:
    """
    延迟加载 entry_points 中注册的 Provider，
    只在第一次调用 get_client 或 get_registered_providers 时执行一次。
    """
    global _entry_points
    if _entry_points is None:
        try:
            # Python 3.10+ 支持按 group 过滤
            _entry_points = entry_points(group='multicloud_storage.providers')
        except TypeError:
            # 兼容旧版 entry_points() 返回全部，需要手动过滤
            _entry_points = [ep for ep in entry_points() if ep.group == 'multicloud_storage.providers']

    # 将所有未注册的 entry_point 通过 ep.load() 注入 _registry
    for ep in _entry_points:
        if ep.name not in _registry:
            _registry[ep.name] = ep.load()

def get_client(provider: str, **kwargs):
    """
    工厂接口：根据 provider 名称实例化并返回对应的 StorageClient。
    :param provider: 注册时用的名称（如 "minio", "oss", "s3_compatible" 或自定义插件名）
    :param kwargs: 传给该客户端 __init__ 的参数
    :return: StorageClient 子类实例
    :raises ValueError: 如果 provider 未注册
    """
    _load_providers()
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
    _load_providers()
    return list(_registry.keys())
