# Copyright (c) 2025, InfinityQ Technology, Inc.

import abc
from io import BytesIO
from typing import Any, Dict, Iterable

import boto3
import boto3.s3
import boto3.s3.transfer
from google.cloud import storage
from google.oauth2 import service_account
from pydantic import BaseModel, ConfigDict, SerializerFunctionWrapHandler, model_serializer
import requests

from titanq._api.model._util import SecretJson, SecretStr
from titanq._api.model.temp_storage import DualUrl


_DOWNLOAD_CHUNK_SIZE = 8192
_TRANSFER_CONFIG = boto3.s3.transfer.TransferConfig(
    multipart_chunksize=5 * 1024 * 1024, # 5 MB
    multipart_threshold=5 * 1024 * 1024, # 5 MB
)


class Location(BaseModel, abc.ABC):
    """ A Location object enables a user to download data from a certain service, uploading is optional """

    @abc.abstractmethod
    def download(self, key: str, bytes_reader: BytesIO) -> None:
        """ download data from a key """

    @abc.abstractmethod
    def download_content_length(self, key: str) -> int:
        """ returns the size of the content of a key to download"""

    @abc.abstractmethod
    def upload(self, key: str, data: BytesIO) -> None:
        """ uploads data to a key, will return if succeeded """


class S3Location(Location):
    """ Simple Storage Service (S3) storage is part of AWS (Amazon Web Services) """
    bucket_name: str
    access_key_id: str
    secret_access_key: SecretStr

    @model_serializer(mode='wrap')
    def serialize_model(self, nxt: SerializerFunctionWrapHandler) -> Dict[str, Any]:
        return {"s3": nxt(self)}

    def _s3_client(self):
        return boto3.client('s3', aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_access_key)

    def download(self, key: str, bytes_reader: BytesIO) -> None:
        client = self._s3_client()
        remote_object = client.get_object(Bucket=self.bucket_name, Key=key)
        body = remote_object['Body']

        while True:
            chunk = body.read(_DOWNLOAD_CHUNK_SIZE)
            if not chunk:
                break
            bytes_reader.write(chunk)

        bytes_reader.seek(0)

    def upload(self, key: str, data: BytesIO):
        client = self._s3_client()
        client.upload_fileobj(data, Bucket=self.bucket_name, Key=key, Config=_TRANSFER_CONFIG)

    def download_content_length(self, key: str) -> int:
        client = self._s3_client()
        response = client.head_object(Bucket=self.bucket_name, Key=key)
        return response['ContentLength']


class GcpLocation(Location):
    """ Google Clous Storage (GCS) is part of GCP (Google Cloud Provider) """
    model_config = ConfigDict(validate_assignment=True)

    bucket_name: str
    json_key: SecretJson

    @model_serializer(mode='wrap')
    def serialize_model(self, nxt: SerializerFunctionWrapHandler) -> Dict[str, Any]:
        return {"gcp": nxt(self)}

    def download(self, key: str, bytes_reader: BytesIO) -> None:
        credentials = service_account.Credentials.from_service_account_info(self.json_key.non_obfuscated_value())
        client = storage.Client(credentials=credentials)
        bucket = client.get_bucket(self.bucket_name)

        blob = bucket.blob(key)
        blob.download_to_file(bytes_reader)
        bytes_reader.seek(0)

    def upload(self, key: str, data: BytesIO):
        raise NotImplementedError(f"Uploading is not currently supported by {self.__class__.__name__}")

    def download_content_length(self, key: str) -> int:
        raise NotImplementedError(f"Obtaining content length is not currenty supported by {self.__class__.__name__}")


class UrlLocation(Location):
    """ Download or upload using an URL """

    @model_serializer(mode='wrap')
    def serialize_model(self, _: SerializerFunctionWrapHandler) -> Dict[str, Any]:
        return { "file_name_is_url": True }

    def download(self, key: str, bytes_reader: BytesIO) -> None:
        with requests.get(key, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=_DOWNLOAD_CHUNK_SIZE):
                if chunk:
                    bytes_reader.write(chunk)

            bytes_reader.seek(0)

    def upload(self, key: str, data: BytesIO):
        response = requests.put(key, data=data)
        response.raise_for_status()

    def download_content_length(self, key: str) -> int:
        response = requests.head(key)
        return int(response.headers.get('Content-Length'))


class TempStorageLocation(UrlLocation):
    """ Temp storage location utilize the temp storage service """
    _url_mapping: Dict[str, DualUrl]

    def __init__(self, dual_urls: Iterable[DualUrl], **kwargs):
        super().__init__(**kwargs)
        self._url_mapping = {}
        for dual_url in dual_urls:
            self._url_mapping[dual_url.upload] = dual_url
            self._url_mapping[dual_url.download] = dual_url

    def download(self, key: str, bytes_reader: BytesIO) -> None:
        download_url = self._url_mapping[key].download
        return super().download(download_url, bytes_reader)

    def download_content_length(self, key: str) -> int:
        download_url = self._url_mapping[key].download
        return super().download_content_length(download_url)

    def upload(self, key: str, data: BytesIO):
        upload_url = self._url_mapping[key].upload
        super().upload(upload_url, data)



class BitBucketLocation(Location):
    """ Bitbucket is a git version control, use it to download files from it """
    repo_name: str
    workspace: str
    access_token: SecretStr
    branch: str

    @model_serializer(mode='wrap')
    def serialize_model(self, nxt: SerializerFunctionWrapHandler) -> Dict[str, Any]:
        return {"bitbucket": nxt(self)}

    def download(self, key: str, bytes_reader: BytesIO) -> None:
        url = self._build_url(key)
        response = self._http_get(url)
        bytes_reader.write(response.content)
        bytes_reader.seek(0)

    def upload(self, key: str, data: BytesIO):
        raise NotImplementedError(f"Uploading is not currently supported by {self.__class__.__name__}")

    def download_content_length(self, key: str) -> int:
        raise NotImplementedError(f"Obtaining content length is not currenty supported by {self.__class__.__name__}")

    def _http_get(self, url: str) -> requests.Response:
        return requests.get(url, headers={"Authorization": f"Bearer {self.access_token.non_obfuscated_value()}"})

    def _build_url(self, key: str) -> str:
        return f"https://api.bitbucket.org/2.0/repositories/{self.workspace}/{self.repo_name}/src/{self.branch}/{key}"
