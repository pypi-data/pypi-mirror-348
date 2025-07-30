import boto3
import base64
import requests
from typing import Dict, Any

class AWSS3:
    def __init__(self, tool_config: Dict[str, Any]):
        """
        :param tool_config: Dict with keys for both auth and bucket config:
            - access_key_id or aws_access_key_id
            - secret_access_key or aws_secret_access_key
            - region or bucket_region
            - bucket_name
            - bucket_file_path
        """
        # Auth
        self.access_key_id = tool_config.get('access_key_id') or tool_config.get('aws_access_key_id')
        self.secret_access_key = tool_config.get('secret_access_key') or tool_config.get('aws_secret_access_key')
        # Bucket
        self.region = tool_config.get('region') or tool_config.get('bucket_region')
        self.bucket_name = tool_config.get('bucket_name')
        self.bucket_file_path = tool_config.get('bucket_file_path', '').rstrip('/')

        self.s3_client = self._init_s3_client()

    def _init_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region
        )

    def upload_document(self, document: str, file_name: str, is_base64: bool = True) -> Dict[str, Any]:
        """
        Uploads a document to S3.
        :param document: base64 string or URL
        :param file_name: Name to use for the file in S3
        :param is_base64: If True, document is base64; if False, document is a URL
        :return: Dict with upload status and S3 URL
        """
        # Get file bytes
        if is_base64:
            file_bytes = base64.b64decode(document)
        else:
            response = requests.get(document)
            response.raise_for_status()
            file_bytes = response.content

        s3_key = f"{self.bucket_file_path}/{file_name}" if self.bucket_file_path else file_name
        print(f"Uploading to S3: {s3_key}")
        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=file_bytes
        )

        s3_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
        return {
            "status": "success",
            "s3_url": s3_url,
            "bucket": self.bucket_name,
            "key": s3_key,
            "data_object_id": file_name,
            "data_object_path": self.bucket_file_path,
            "data_warehouse_name": "AWS S3"
        }

    def fetch_document(self, file_name: str, file_path: str) -> bytes:
        """
        Fetches a file from S3 and returns its bytes.
        :param file_name: The name of the file (e.g., 'mydoc.pdf')
        :param file_path: The S3 key or prefix (e.g., 'folder1/folder2')
        :return: File content as bytes
        """
        # Compose the full S3 key
        if file_path:
            s3_key = f"{file_path.rstrip('/')}/{file_name}"
        else:
            s3_key = file_name

        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
        return response['Body'].read()
