"""阿里云OSS处理器"""

import oss2
from ocsh.handlers.base_handler import BaseHandler


class OssHandler(BaseHandler):
    """
    阿里云OSS处理器
    """
    def __init__(self,access_key_id: str, access_key_secret: str, endpoint: str, bucket_name: str):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def upload(self, object_name, file_path):
        """
        上传到OSS
        """
        try:
            result = self.bucket.put_object_from_file(object_name, file_path)

        except Exception as e:
            print(f"文件上传失败：{e}")

    def download(self, object_name, file_path):
        """
        从OSS下载文件
        """
        try:
            result = self.bucket.get_object_to_file(object_name, file_path)
            if result.status == 200:
                print(f"{file_path}")
        except Exception as e:
            print(f"下载文件失败: {e}")

    def delete(self, object_name):
        """
        从OSS删除文件
        """
        try:
            result = self.bucket.delete_object(object_name)
            if result.status == 204:
                print("DONE")
        except Exception as e:
            print(f"删除文件失败: {e}")