from logging import Logger
from typing import Iterator
from fastapi import HTTPException
from minio import Minio
from minio.error import S3Error
from io import BytesIO

from corelib.utils.configuration_builder import Settings


class MinioUtility():
    """
    Utility class that provides common functinality for Minio
    """

    client:Minio = None
    logger:Logger = None
    def __init__(self, settings:Settings,logger:Logger):
        self.client = Minio(settings.minio_url,
                            access_key=settings.minio_access_key,
                            secret_key= settings.minio_secret_key)
        self.logger = logger
    
    def bucket_exists(self,bucket_name):
        return self.client.bucket_exists(bucket_name)
    
    def create_bucket(self,bucket_name):
        self.logger.info(f"Creating bucket {bucket_name}")
        self.client.make_bucket(bucket_name=bucket_name)
        self.logger.info(f"Successfully created bucket {bucket_name}")

    def list_buckets(self)->list[any]:
        buckets = self.client.list_buckets()
        return buckets

    def list_objects_in_bucket(self,bucket_name,recursive:bool = True,start_after="")->Iterator[any]:
        if not self.bucket_exists(bucket_name):
            raise Exception(f"Bucket {bucket_name} not found")

        objects = self.client.list_objects(
            bucket_name, recursive=recursive, start_after=start_after,
        )

        return objects


    def upload_file(self, bucket_name:str, file:BytesIO ,dest_file_name:str, create_bucket_if_not_exist=True):

        if not self.bucket_exists(bucket_name=bucket_name):
            if create_bucket_if_not_exist:
                self.create_bucket(bucket_name=bucket_name)
            else:
                raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} not found")
        
        upl = self.client.fput_object(bucket_name,dest_file_name,file)
        self.logger.info(f"Succesfully uploaded file {dest_file_name}")
        return upl
    
    def download_file(self,bucket_name:str,file_name:str):
        if not self.bucket_exists(bucket_name):
            raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} not found")
        
        bucket_objects = list(self.list_objects_in_bucket(bucket_name))

        for o in bucket_objects:
            t = o
        
        file = self.client.fget_object(bucket_name, file_name)
        return file
    
    def delete_file(self,bucket_name:str,file_name:str):
        if not self.bucket_exists(bucket_name):
            raise HTTPException(status_code=404, detail=f"Bucket {bucket_name} not found")
        
        self.client.remove_object(bucket_name, file_name)

        

    
