# 强制把这些类导入进来，打包器就看得到模块依赖了
from .clients.minio_client      import MinioClient
from .clients.oss_client_v2     import OSSV2Client
from .clients.s3_compat_client  import S3CompatClient