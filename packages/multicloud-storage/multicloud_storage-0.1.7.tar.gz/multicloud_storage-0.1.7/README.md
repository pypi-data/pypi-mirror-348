## 概述

`multicloud-storage` 是一个通用的 Python 存储客户端库，可统一对接 MinIO、阿里 OSS（v2 SDK）及任意 S3 兼容服务。

- 支持：文件上传、下载、删除、预签名 URL，批量／分页列举，目录级删除，以及对象存在性检测。
- 内置：对 AWS S3、MinIO、阿里 OSS v2 与七牛等兼容服务的自动识别与适配，极大简化多云环境下的存储操作。

------

## 安装

```bash
# 从 PyPI 安装最新版本
pip install multicloud-storage

# 或者克隆到本地开发、可编辑安装
git clone https://github.com/your_username/multicloud-storage.git
cd multicloud-storage
pip install -r requirements.txt
pip install -e .

# 或者在 requirements.txt 中，增加如下依赖
# 最低版本 0.1.2，兼容 0.1.x 
# ~=0.1.2：当前包会自动拿到 0.1.3、0.1.4 … 直到 0.2.0 之前的最新版本
# multicloud-storage~=0.1.2 等同于 >=0.1.2, <0.2.0，是 PEP 440 中的“兼容版本”写法
multicloud-storage~=0.1.2
# 使用 --upgrade（或简写 -U）参数，强制 pip 将已安装的包升级到符合版本约束的新版本
pip install --upgrade -r requirements.txt
# 单独升级 multicloud-storage，pip 会查找最新的符合版本约束（>=0.1.2,<0.2.0）并安装 
pip install --upgrade multicloud-storage~=0.1.2
# 验证安装结果
pip show multicloud-storage
```

------

## 目录说明

```text
.
├── README.md                  # 项目主说明（可替换为本文件）
├── setup.py                   # 打包安装脚本
├── requirements.txt           # 依赖列表
│
├── docs/                      # 额外文档
│   └── s3api说明.md           # S3 API 相关说明
│
├── examples/                  # 使用示例
│   ├── README.md              # 示例说明
│   ├── minio_example.py       # MinIO 使用示例
│   ├── oss_example.py         # 阿里 OSS v2 示例
│   ├── s3_example.py          # AWS S3 / 兼容示例
│   ├── page_example.py        # 分页列举示例
│   ├── usage_example.py       # 综合使用示例
│   └── raw_sdk_example.py     # 直接调用底层 SDK 示例
│
├── multicloud_storage/        # 源码主包
│   ├── clients/               # 各厂商客户端实现
│   │   ├── minio_client.py
│   │   ├── oss_client_v2.py
│   │   └── s3_compat_client.py
│   └── core/                  # 核心抽象与工具
│       ├── base.py            # 抽象基类 StorageClient
│       ├── factory.py         # 客户端工厂 create_storage_client
│       ├── registry.py        # 注册表与 entry_points 加载
│       ├── providers.py       # provider 常量定义
│       ├── result.py          # UploadResult、ListObjectsResult、ObjectInfo
│       ├── exceptions.py      # 自定义异常
│       ├── url_parser.py      # storage_url 解析
│       └── utils.py           # content-type 检测等工具
│
└── test/                      # 测试用例
    └── test_storage/          # 存储相关测试脚本
        ├── test_storage.py    # 基本上传/下载/生成 URL 测试
        ├── test_page.py       # list_objects 分页测试
        ├── test_delete.py     # 单文件删除测试
        ├── test_delete_prefix.py # 目录级删除测试
        └── test_exists.py     # exists 方法测试
```

------

## 快速开始

```python
from multicloud_storage.core.factory import create_storage_client
from multicloud_storage.core.providers import MINIO, OSS, S3_COMPATIBLE

# 示例：通过 storage_url 一行初始化 MinIO 客户端
client = create_storage_client(
    provider=MINIO,
    storage_url=(
        "http://MINIO_AK:MINIO_SK"
        "@minio.example.com:9000/my-bucket/videos"
    )
)

# 上传文件
result = client.upload_file("local.mp4", "2025/05/local.mp4")
print("上传成功：", result.url)

# 列举前缀
page = client.list_objects(prefix="2025/05", max_items=100)
for obj in page.objects:
    print(obj.key, obj.size, obj.last_modified)

# 生成预签名 URL
url = client.generate_presigned_url("2025/05/local.mp4", expires_in=600)
print("预签名访问：", url)

# 删除目录下所有对象
client.delete_prefix("2025/05/")

# 检查对象是否存在
info = client.exists("2025/05/local.mp4")
if info:
    print("已存在，URL=", info.url)
else:
    print("不存在")
```

------

## 示例脚本

目录 `examples/` 下包含多种脚本：

- `minio_example.py`、`oss_example.py`、`s3_example.py`：分别针对不同服务的独立演示。
- `page_example.py`：分页列举示例。
- `usage_example.py`：综合调用上传、下载、删除、预签名、exists。
- `raw_sdk_example.py`：拿到底层 SDK（`client.raw_client`）直接调用。

------

## 测试

项目已集成多份测试，使用方法：

```bash
pytest -q test/test_storage
```

- `test_storage.py` 检查基础功能（上传、下载、URL）。
- `test_page.py` 检查分页列举与排序。
- `test_delete.py` / `test_delete_prefix.py` 检查单文件和目录删除。
- `test_exists.py` 检查 exists 接口。

------

## 贡献与发布

1. **发布新版本**

   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```
   
2. **贡献指南**

   - Fork 本仓库、在 `feature/` 分支上开发、提交 PR。
   - 新增功能请补充对应测试用例，并在 `examples/` 添加演示脚本。
   - 遵守 PEP8，确保类型注释与文档完整。

3. **更多文档**

   - `docs/s3api说明.md`：S3 REST API 细节对照。
   - `examples/README.md`：各示例脚本使用说明。

------

感谢使用 `multicloud-storage`，如有问题欢迎提 issue 或加入讨论！