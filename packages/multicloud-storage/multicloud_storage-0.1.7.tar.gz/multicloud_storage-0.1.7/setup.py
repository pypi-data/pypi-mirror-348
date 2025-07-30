import setuptools

# ──────────────────────────────────────────────────────────────────────────────
# setuptools.setup() 调用
#    - name/version/description 等元信息
#    - packages 自动发现源码包
#    - install_requires 必须是显式静态的，不要动态读取，否则无法写入 whl 中
#    - entry_points 注册内置 provider，让用户在不 import 具体模块的情况下也能用插件机制扩展
#    - python_requires 限定最低 Python 版本
# ──────────────────────────────────────────────────────────────────────────────
setuptools.setup(
    name="multicloud-storage",                # pip install 时的包名
    version="0.1.7",                          # 请在每次发布前手动更新版本号
    description="统一操作 MinIO/OSS/S3 兼容存储的工具包",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/your_username/multicloud-storage",

    # 只打包 multicloud_storage 及其所有子包
    packages=setuptools.find_packages(
        include=["multicloud_storage", "multicloud_storage.*"]
    ),

    # ───────────────────────────────────────────────────
    # 关键：静态列出所有运行时依赖（否则 whl 中不会加入依赖）
    # ───────────────────────────────────────────────────
    install_requires=[
        "boto3>=1.38.9",
        "alibabacloud_oss_v2>=1.1.1",
        "minio>=7.2.15",
        "importlib_metadata~=8.7.0; python_version < '3.8'",
        "python-magic>=0.4.27; sys_platform != 'win32'",
        "python-magic-bin>=0.4.14; sys_platform == 'win32'",
    ],

    # 限定 Python 版本
    python_requires=">=3.6",

    # 插件式扩展：将内置的三种 provider 注册到 multicloud_storage.providers entry point
    entry_points={
        "multicloud_storage.providers": [
            "minio          = multicloud_storage.clients.minio_client:MinioClient",
            "oss            = multicloud_storage.clients.oss_client_v2:OSSV2Client",
            "s3_compatible  = multicloud_storage.clients.s3_compat_client:S3CompatClient",
        ]
    },

    # 保证 metadata（包括 entry_points）解压到文件系统，不会被打包成 zip/egg
    zip_safe=False,

    # PyPI 分类，用于让用户快速筛选
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
