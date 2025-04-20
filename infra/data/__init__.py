import aioboto3

from infra import Config


class Data:
    def __init__(self, config: Config):
        self.__session = aioboto3.Session()
        self.__config = config

    async def get_object(self, name):
        async with self.__session.resource(
            "s3",
            endpoint_url=self.__config.data_endpoint,
            aws_access_key_id=self.__config.data_ak,
            aws_secret_access_key=self.__config.data_sk,
        ) as s3:
            bucket = await s3.Bucket(self.__config.data_bucket)
            async for s3_object in bucket.objects.all():
                print(s3_object)


