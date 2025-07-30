"""处理器基类"""

from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def upload(self, object_name, file_path):
        """
        上传文件

        Args:
            object_name: 云存储中的对象名称
            file_path: 本地文件路径
        """
        pass

    @abstractmethod
    def download(self, object_name, file_path):
        """
        下载文件

        Args:
            object_name: 云存储中的对象名称
            file_path: 本地文件路径
        """
        pass

    @abstractmethod
    def delete(self, object_name):
        """
        删除文件

        Args:
            object_name: 云存储中的对象名称
        """
        pass