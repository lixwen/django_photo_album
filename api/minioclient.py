from django.conf import settings
from minio import Minio

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)


def upload_to_minio(file_path, object_name, bucket_name):
    return minio_client.fput_object(bucket_name, object_name, file_path)


# def upload_to_minio(data, object_name, bucket_name, length):
#     return minio_client.put_object(bucket_name, object_name, data, length)

def download_from_minio(object_name, bucket_name):
    response = minio_client.get_object(bucket_name, object_name)
    return response.read()


def get_minio_url(object_name, bucket_name):
    return minio_client.presigned_get_object(bucket_name, object_name)


def generate_thumbnail(file_path, thumbnail_path):
    # 生成缩略图的逻辑，可以使用PIL库或者其他缩略图生成工具
    pass
