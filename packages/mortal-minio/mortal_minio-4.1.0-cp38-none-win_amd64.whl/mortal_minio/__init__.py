#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 15:31
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .minio_main import MortalMinioMain


class MortalMinio(MortalMinioMain):
    """
    MortalMinio 类继承自 MortalMinioMain，用于管理与 MinIO 存储服务的交互。
    """
    def __init__(self, config):
        """
        初始化 MortalMinio 实例。

        :param config: 配置信息，用于初始化 MinIO 客户端。
        """
        super().__init__(config)

    def connect(self):
        """
        连接到 MinIO 服务器。
        """
        self._connect()

    def create_bucket(self, bucket_name, location="cn-north-1", object_lock=False):
        """
        创建一个新的存储桶。

        :param bucket_name: 存储桶名称。
        :param location: 存储桶所在区域，默认为 "cn-north-1"。
        :param object_lock: 是否启用对象锁定，默认为 False。
        :return: 创建结果。
        """
        return self._create_bucket(bucket_name, location, object_lock)

    def remove_bucket(self, bucket_name):
        """
        删除指定的存储桶。

        :param bucket_name: 要删除的存储桶名称。
        :return: 删除结果。
        """
        return self._remove_bucket(bucket_name)

    def bucket_list(self):
        """
        获取所有存储桶的列表。

        :return: 存储桶列表。
        """
        return self._bucket_list()

    def bucket_list_files(self, bucket_name, prefix=""):
        """
        列出指定存储桶中的文件。

        :param bucket_name: 存储桶名称。
        :param prefix: 文件前缀，默认为空字符串。
        :return: 文件列表。
        """
        return self._bucket_list_files(bucket_name, prefix)

    def bucket_policy(self, bucket_name):
        """
        获取指定存储桶的策略。

        :param bucket_name: 存储桶名称。
        :return: 存储桶策略。
        """
        return self._bucket_policy(bucket_name)

    def upload_flow(self, bucket_name, object_name, data):
        """
        上传数据流到指定存储桶。

        :param bucket_name: 存储桶名称。
        :param object_name: 对象名称。
        :param data: 要上传的数据。
        """
        self._upload_flow(bucket_name, object_name, data)

    def upload_file(self, bucket_name, object_name, file_name, parallel=3):
        """
        上传文件到指定存储桶。

        :param bucket_name: 存储桶名称。
        :param object_name: 对象名称。
        :param file_name: 本地文件路径。
        :param parallel: 并行上传的线程数，默认为 3。
        """
        self._upload_file(bucket_name, object_name, file_name, parallel)

    def upload_dir(self, bucket_name, dir_path, parallel=3, base_dir=None):
        """
        上传目录中的所有文件到指定存储桶。

        :param bucket_name: 存储桶名称。
        :param dir_path: 本地目录路径。
        :param parallel: 并行上传的线程数，默认为 3。
        :param base_dir: 基础目录路径，默认为 None。
        """
        self._upload_dir(bucket_name, dir_path, parallel, base_dir)

    def download_flow(self, bucket_name, object_name):
        """
        从指定存储桶下载数据流。

        :param bucket_name: 存储桶名称。
        :param object_name: 对象名称。
        :return: 下载的数据流。
        """
        return self._download_flow(bucket_name, object_name)

    def download_file(self, bucket_name, object_name, file_name):
        """
        从指定存储桶下载文件。

        :param bucket_name: 存储桶名称。
        :param object_name: 对象名称。
        :param file_name: 本地文件保存路径。
        :return: 下载的文件。
        """
        return self._download_file(bucket_name, object_name, file_name)

    def download_dir(self, bucket_name, object_path, dir_path):
        """
        从指定存储桶下载目录中的所有文件。

        :param bucket_name: 存储桶名称。
        :param object_path: 对象路径。
        :param dir_path: 本地目录保存路径。
        """
        self._download_dir(bucket_name, object_path, dir_path)

    def remove_object(self, bucket_name, object_name):
        """
        删除指定存储桶中的对象。

        :param bucket_name: 存储桶名称。
        :param object_name: 对象名称。
        """
        self._remove_object(bucket_name, object_name)

    def remove_objects(self, bucket_name, object_list):
        """
        删除指定存储桶中的多个对象。

        :param bucket_name: 存储桶名称。
        :param object_list: 要删除的对象列表。
        """
        self._remove_objects(bucket_name, object_list)

    def get_url(self, bucket, object_name, days=7):
        """
        获取指定对象的临时访问 URL。

        :param bucket: 存储桶名称。
        :param object_name: 对象名称。
        :param days: URL 的有效期，默认为 7 天。
        :return: 临时访问 URL。
        """
        return self._get_url(bucket, object_name, days)
