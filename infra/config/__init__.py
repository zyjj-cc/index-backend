import os


class Config:
    def __init__(self):
        self.db_url = os.getenv('db_url')
        self.db_username = os.getenv('db_username')
        self.db_password = os.getenv('db_password')
        self.db_namespace = os.getenv('db_namespace')
        self.db_name = os.getenv('db_name')

        self.data_endpoint = os.getenv('minio_endpoint')
        self.data_ak = os.getenv('minio_ak')
        self.data_sk = os.getenv('minio_sk')
        self.data_bucket = os.getenv('minio_bucket')

