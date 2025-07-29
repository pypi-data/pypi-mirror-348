# -*- coding: utf-8 -*-
# @Author: Erin & Joanne
# @Date:   2024-02-11 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-02-18 14:53:37
# @Description: Provides method retrieve metadata from aws buckets and objects.

import boto3
import os
from gailbot.pluginSuiteManager.APIConsumer import APIConsumer
from threading import Lock

class S3BucketManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(S3BucketManager, cls).__new__(cls)
                    api_consumer = APIConsumer.get_instance()
                    response = api_consumer.fetch_secrets()
                    cls._instance.aws_api_key = response['aws_api_key']
                    cls._instance.aws_api_id = response['aws_api_id']

                    print(f"aws_api_key: {cls._instance.aws_api_key}")
                    print(f"aws_api_id: {cls._instance.aws_api_id}")
        return cls._instance
        
    @classmethod
    def get_instance(cls):
        # if it doesn't exist yet, calling cls() will run __new__
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None

    # Retrieve and return the version of the bucket
    # TODO: exceptions are not catched here. Caller expected to catch exceptions
    def get_remote_version(self, bucket_name, object_name) -> str:
        """
        If bucket_name and object_name identifies an existing object in aws s3 bucket, and the
        object has s3 remote metadata for version, returns the updated version of the object

        Parameters
        ----------
        bucket_name
        object_name

        Returns
        -------
        str

        Raises
        -------

        """
        s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_api_id,
            aws_secret_access_key=self.aws_api_key,
        )

        s3_object = s3.head_object(Bucket=bucket_name, Key=object_name)
        object_metadata = s3_object["Metadata"]

        return object_metadata["version"]
    
    def get_s3(self):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_api_id,
            aws_secret_access_key=self.aws_api_key,
        )

        return s3
    
    def get_r3(self):
        r3 = boto3.resource(
            "s3",             
            aws_access_key_id=self.aws_api_id,
            aws_secret_access_key=self.aws_api_key,
        )

        return r3