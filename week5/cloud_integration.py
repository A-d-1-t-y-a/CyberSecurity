#!/usr/bin/env python3
"""
Week 5 Cloud Integration Script
Cross-Platform Unified Memory Forensics Framework
Student: Manoj Santhoju (ID: 23394544)
Institution: National College of Ireland
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import json
from datetime import datetime
import boto3
import requests
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('week5/logs/cloud_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week5CloudIntegration:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.cloud_config = self._load_cloud_config()
        
    def _load_cloud_config(self):
        """Load cloud configuration"""
        config_file = self.script_dir / 'data' / 'cloud_config.json'
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create default cloud configuration
            default_config = {
                "aws": {
                    "enabled": False,
                    "region": "us-east-1",
                    "bucket": "memory-forensics-dumps",
                    "access_key": "",
                    "secret_key": ""
                },
                "azure": {
                    "enabled": False,
                    "account_name": "",
                    "account_key": "",
                    "container": "memory-dumps"
                },
                "gcp": {
                    "enabled": False,
                    "project_id": "",
                    "bucket": "memory-forensics-dumps",
                    "credentials": ""
                }
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
                
            return default_config
            
    def test_aws_integration(self):
        """Test AWS S3 integration"""
        logger.info("Testing AWS S3 integration...")
        
        if not self.cloud_config.get("aws", {}).get("enabled", False):
            logger.info("AWS integration disabled")
            return {"status": "disabled", "message": "AWS integration not enabled"}
            
        try:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.cloud_config["aws"]["access_key"],
                aws_secret_access_key=self.cloud_config["aws"]["secret_key"],
                region_name=self.cloud_config["aws"]["region"]
            )
            
            # Test bucket access
            bucket_name = self.cloud_config["aws"]["bucket"]
            response = s3_client.head_bucket(Bucket=bucket_name)
            
            # Test upload
            test_file = self.script_dir / 'data' / 'test_upload.txt'
            with open(test_file, 'w') as f:
                f.write("Test upload for memory forensics framework")
                
            s3_client.upload_file(str(test_file), bucket_name, 'test/test_upload.txt')
            
            # Test download
            download_path = self.script_dir / 'data' / 'test_download.txt'
            s3_client.download_file(bucket_name, 'test/test_upload.txt', str(download_path))
            
            # Cleanup
            s3_client.delete_object(Bucket=bucket_name, Key='test/test_upload.txt')
            test_file.unlink()
            download_path.unlink()
            
            return {
                "status": "success",
                "message": "AWS S3 integration working correctly",
                "bucket": bucket_name,
                "region": self.cloud_config["aws"]["region"]
            }
            
        except Exception as e:
            logger.error(f"AWS integration test failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def test_azure_integration(self):
        """Test Azure Blob Storage integration"""
        logger.info("Testing Azure Blob Storage integration...")
        
        if not self.cloud_config.get("azure", {}).get("enabled", False):
            logger.info("Azure integration disabled")
            return {"status": "disabled", "message": "Azure integration not enabled"}
            
        try:
            from azure.storage.blob import BlobServiceClient
            
            # Initialize Azure client
            account_name = self.cloud_config["azure"]["account_name"]
            account_key = self.cloud_config["azure"]["account_key"]
            container_name = self.cloud_config["azure"]["container"]
            
            blob_service_client = BlobServiceClient(
                account_url=f"https://{account_name}.blob.core.windows.net",
                credential=account_key
            )
            
            # Test container access
            container_client = blob_service_client.get_container_client(container_name)
            
            # Test upload
            test_file = self.script_dir / 'data' / 'test_azure_upload.txt'
            with open(test_file, 'w') as f:
                f.write("Test upload for memory forensics framework")
                
            blob_client = container_client.get_blob_client("test/test_azure_upload.txt")
            with open(test_file, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
                
            # Test download
            download_path = self.script_dir / 'data' / 'test_azure_download.txt'
            with open(download_path, 'wb') as download_file:
                download_file.write(blob_client.download_blob().readall())
                
            # Cleanup
            blob_client.delete_blob()
            test_file.unlink()
            download_path.unlink()
            
            return {
                "status": "success",
                "message": "Azure Blob Storage integration working correctly",
                "container": container_name,
                "account": account_name
            }
            
        except Exception as e:
            logger.error(f"Azure integration test failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def test_gcp_integration(self):
        """Test Google Cloud Storage integration"""
        logger.info("Testing Google Cloud Storage integration...")
        
        if not self.cloud_config.get("gcp", {}).get("enabled", False):
            logger.info("GCP integration disabled")
            return {"status": "disabled", "message": "GCP integration not enabled"}
            
        try:
            from google.cloud import storage
            
            # Initialize GCP client
            project_id = self.cloud_config["gcp"]["project_id"]
            bucket_name = self.cloud_config["gcp"]["bucket"]
            
            client = storage.Client(project=project_id)
            bucket = client.bucket(bucket_name)
            
            # Test upload
            test_file = self.script_dir / 'data' / 'test_gcp_upload.txt'
            with open(test_file, 'w') as f:
                f.write("Test upload for memory forensics framework")
                
            blob = bucket.blob('test/test_gcp_upload.txt')
            blob.upload_from_filename(str(test_file))
            
            # Test download
            download_path = self.script_dir / 'data' / 'test_gcp_download.txt'
            blob.download_to_filename(str(download_path))
            
            # Cleanup
            blob.delete()
            test_file.unlink()
            download_path.unlink()
            
            return {
                "status": "success",
                "message": "Google Cloud Storage integration working correctly",
                "bucket": bucket_name,
                "project": project_id
            }
            
        except Exception as e:
            logger.error(f"GCP integration test failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def create_cloud_handler(self):
        """Create cloud handler implementation"""
        logger.info("Creating cloud handler...")
        
        cloud_handler_file = self.project_root / 'src' / 'cloud' / 'cloud_handler.py'
        with open(cloud_handler_file, 'w', encoding='utf-8') as f:
            f.write(self._get_cloud_handler_implementation())
            
        logger.info("Cloud handler created")
        
    def _get_cloud_handler_implementation(self):
        """Get cloud handler implementation"""
        return '''"""
Cloud Handler for Memory Forensics Framework
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import boto3
from azure.storage.blob import BlobServiceClient
from google.cloud import storage
import requests
import time

logger = logging.getLogger(__name__)

class CloudHandler:
    """
    Handles cloud storage operations for memory forensics framework
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize cloud handler
        
        Args:
            config: Cloud configuration dictionary
        """
        self.config = config or {}
        self.aws_client = None
        self.azure_client = None
        self.gcp_client = None
        
        self._initialize_clients()
        
        logger.info("CloudHandler initialized")
        
    def _initialize_clients(self):
        """Initialize cloud storage clients"""
        # Initialize AWS S3 client
        if self.config.get("aws", {}).get("enabled", False):
            try:
                self.aws_client = boto3.client(
                    's3',
                    aws_access_key_id=self.config["aws"]["access_key"],
                    aws_secret_access_key=self.config["aws"]["secret_key"],
                    region_name=self.config["aws"]["region"]
                )
                logger.info("AWS S3 client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AWS client: {e}")
                
        # Initialize Azure Blob Storage client
        if self.config.get("azure", {}).get("enabled", False):
            try:
                account_name = self.config["azure"]["account_name"]
                account_key = self.config["azure"]["account_key"]
                
                self.azure_client = BlobServiceClient(
                    account_url=f"https://{account_name}.blob.core.windows.net",
                    credential=account_key
                )
                logger.info("Azure Blob Storage client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Azure client: {e}")
                
        # Initialize Google Cloud Storage client
        if self.config.get("gcp", {}).get("enabled", False):
            try:
                project_id = self.config["gcp"]["project_id"]
                self.gcp_client = storage.Client(project=project_id)
                logger.info("Google Cloud Storage client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize GCP client: {e}")
                
    def upload_dump(self, dump_path: str, cloud_path: str, 
                   provider: str = "aws") -> Dict[str, Any]:
        """
        Upload memory dump to cloud storage
        
        Args:
            dump_path: Local path to memory dump
            cloud_path: Cloud storage path
            provider: Cloud provider (aws, azure, gcp)
            
        Returns:
            Upload result dictionary
        """
        logger.info(f"Uploading dump to {provider}: {cloud_path}")
        
        try:
            if provider == "aws" and self.aws_client:
                return self._upload_to_aws(dump_path, cloud_path)
            elif provider == "azure" and self.azure_client:
                return self._upload_to_azure(dump_path, cloud_path)
            elif provider == "gcp" and self.gcp_client:
                return self._upload_to_gcp(dump_path, cloud_path)
            else:
                raise ValueError(f"Unsupported provider or client not initialized: {provider}")
                
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _upload_to_aws(self, dump_path: str, cloud_path: str) -> Dict[str, Any]:
        """Upload to AWS S3"""
        try:
            bucket_name = self.config["aws"]["bucket"]
            
            # Upload file
            self.aws_client.upload_file(dump_path, bucket_name, cloud_path)
            
            # Get file info
            response = self.aws_client.head_object(Bucket=bucket_name, Key=cloud_path)
            
            return {
                "status": "success",
                "provider": "aws",
                "bucket": bucket_name,
                "key": cloud_path,
                "size": response.get("ContentLength", 0),
                "upload_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AWS upload failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _upload_to_azure(self, dump_path: str, cloud_path: str) -> Dict[str, Any]:
        """Upload to Azure Blob Storage"""
        try:
            container_name = self.config["azure"]["container"]
            container_client = self.azure_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(cloud_path)
            
            # Upload file
            with open(dump_path, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
                
            # Get blob properties
            properties = blob_client.get_blob_properties()
            
            return {
                "status": "success",
                "provider": "azure",
                "container": container_name,
                "blob": cloud_path,
                "size": properties.size,
                "upload_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Azure upload failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _upload_to_gcp(self, dump_path: str, cloud_path: str) -> Dict[str, Any]:
        """Upload to Google Cloud Storage"""
        try:
            bucket_name = self.config["gcp"]["bucket"]
            bucket = self.gcp_client.bucket(bucket_name)
            blob = bucket.blob(cloud_path)
            
            # Upload file
            blob.upload_from_filename(dump_path)
            
            # Get blob info
            blob.reload()
            
            return {
                "status": "success",
                "provider": "gcp",
                "bucket": bucket_name,
                "blob": cloud_path,
                "size": blob.size,
                "upload_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"GCP upload failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def download_dump(self, cloud_path: str, local_path: str, 
                     provider: str = "aws") -> Dict[str, Any]:
        """
        Download memory dump from cloud storage
        
        Args:
            cloud_path: Cloud storage path
            local_path: Local download path
            provider: Cloud provider (aws, azure, gcp)
            
        Returns:
            Download result dictionary
        """
        logger.info(f"Downloading dump from {provider}: {cloud_path}")
        
        try:
            if provider == "aws" and self.aws_client:
                return self._download_from_aws(cloud_path, local_path)
            elif provider == "azure" and self.azure_client:
                return self._download_from_azure(cloud_path, local_path)
            elif provider == "gcp" and self.gcp_client:
                return self._download_from_gcp(cloud_path, local_path)
            else:
                raise ValueError(f"Unsupported provider or client not initialized: {provider}")
                
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _download_from_aws(self, cloud_path: str, local_path: str) -> Dict[str, Any]:
        """Download from AWS S3"""
        try:
            bucket_name = self.config["aws"]["bucket"]
            
            # Download file
            self.aws_client.download_file(bucket_name, cloud_path, local_path)
            
            # Get file info
            local_size = os.path.getsize(local_path)
            
            return {
                "status": "success",
                "provider": "aws",
                "local_path": local_path,
                "size": local_size,
                "download_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AWS download failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _download_from_azure(self, cloud_path: str, local_path: str) -> Dict[str, Any]:
        """Download from Azure Blob Storage"""
        try:
            container_name = self.config["azure"]["container"]
            container_client = self.azure_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(cloud_path)
            
            # Download file
            with open(local_path, 'wb') as download_file:
                download_file.write(blob_client.download_blob().readall())
                
            # Get file info
            local_size = os.path.getsize(local_path)
            
            return {
                "status": "success",
                "provider": "azure",
                "local_path": local_path,
                "size": local_size,
                "download_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Azure download failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _download_from_gcp(self, cloud_path: str, local_path: str) -> Dict[str, Any]:
        """Download from Google Cloud Storage"""
        try:
            bucket_name = self.config["gcp"]["bucket"]
            bucket = self.gcp_client.bucket(bucket_name)
            blob = bucket.blob(cloud_path)
            
            # Download file
            blob.download_to_filename(local_path)
            
            # Get file info
            local_size = os.path.getsize(local_path)
            
            return {
                "status": "success",
                "provider": "gcp",
                "local_path": local_path,
                "size": local_size,
                "download_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"GCP download failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def list_dumps(self, provider: str = "aws", prefix: str = "") -> List[Dict[str, Any]]:
        """
        List memory dumps in cloud storage
        
        Args:
            provider: Cloud provider (aws, azure, gcp)
            prefix: Path prefix to filter results
            
        Returns:
            List of dump information dictionaries
        """
        logger.info(f"Listing dumps from {provider}")
        
        try:
            if provider == "aws" and self.aws_client:
                return self._list_aws_dumps(prefix)
            elif provider == "azure" and self.azure_client:
                return self._list_azure_dumps(prefix)
            elif provider == "gcp" and self.gcp_client:
                return self._list_gcp_dumps(prefix)
            else:
                raise ValueError(f"Unsupported provider or client not initialized: {provider}")
                
        except Exception as e:
            logger.error(f"List dumps failed: {e}")
            return []
            
    def _list_aws_dumps(self, prefix: str) -> List[Dict[str, Any]]:
        """List dumps from AWS S3"""
        try:
            bucket_name = self.config["aws"]["bucket"]
            
            response = self.aws_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix
            )
            
            dumps = []
            for obj in response.get('Contents', []):
                dumps.append({
                    "name": obj['Key'],
                    "size": obj['Size'],
                    "modified": obj['LastModified'].isoformat(),
                    "provider": "aws"
                })
                
            return dumps
            
        except Exception as e:
            logger.error(f"AWS list dumps failed: {e}")
            return []
            
    def _list_azure_dumps(self, prefix: str) -> List[Dict[str, Any]]:
        """List dumps from Azure Blob Storage"""
        try:
            container_name = self.config["azure"]["container"]
            container_client = self.azure_client.get_container_client(container_name)
            
            blobs = container_client.list_blobs(name_starts_with=prefix)
            
            dumps = []
            for blob in blobs:
                dumps.append({
                    "name": blob.name,
                    "size": blob.size,
                    "modified": blob.last_modified.isoformat(),
                    "provider": "azure"
                })
                
            return dumps
            
        except Exception as e:
            logger.error(f"Azure list dumps failed: {e}")
            return []
            
    def _list_gcp_dumps(self, prefix: str) -> List[Dict[str, Any]]:
        """List dumps from Google Cloud Storage"""
        try:
            bucket_name = self.config["gcp"]["bucket"]
            bucket = self.gcp_client.bucket(bucket_name)
            
            blobs = bucket.list_blobs(prefix=prefix)
            
            dumps = []
            for blob in blobs:
                dumps.append({
                    "name": blob.name,
                    "size": blob.size,
                    "modified": blob.time_created.isoformat(),
                    "provider": "gcp"
                })
                
            return dumps
            
        except Exception as e:
            logger.error(f"GCP list dumps failed: {e}")
            return []
            
    def delete_dump(self, cloud_path: str, provider: str = "aws") -> Dict[str, Any]:
        """
        Delete memory dump from cloud storage
        
        Args:
            cloud_path: Cloud storage path
            provider: Cloud provider (aws, azure, gcp)
            
        Returns:
            Delete result dictionary
        """
        logger.info(f"Deleting dump from {provider}: {cloud_path}")
        
        try:
            if provider == "aws" and self.aws_client:
                return self._delete_from_aws(cloud_path)
            elif provider == "azure" and self.azure_client:
                return self._delete_from_azure(cloud_path)
            elif provider == "gcp" and self.gcp_client:
                return self._delete_from_gcp(cloud_path)
            else:
                raise ValueError(f"Unsupported provider or client not initialized: {provider}")
                
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _delete_from_aws(self, cloud_path: str) -> Dict[str, Any]:
        """Delete from AWS S3"""
        try:
            bucket_name = self.config["aws"]["bucket"]
            
            self.aws_client.delete_object(Bucket=bucket_name, Key=cloud_path)
            
            return {
                "status": "success",
                "provider": "aws",
                "deleted_path": cloud_path,
                "delete_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AWS delete failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _delete_from_azure(self, cloud_path: str) -> Dict[str, Any]:
        """Delete from Azure Blob Storage"""
        try:
            container_name = self.config["azure"]["container"]
            container_client = self.azure_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(cloud_path)
            
            blob_client.delete_blob()
            
            return {
                "status": "success",
                "provider": "azure",
                "deleted_path": cloud_path,
                "delete_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Azure delete failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def _delete_from_gcp(self, cloud_path: str) -> Dict[str, Any]:
        """Delete from Google Cloud Storage"""
        try:
            bucket_name = self.config["gcp"]["bucket"]
            bucket = self.gcp_client.bucket(bucket_name)
            blob = bucket.blob(cloud_path)
            
            blob.delete()
            
            return {
                "status": "success",
                "provider": "gcp",
                "deleted_path": cloud_path,
                "delete_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"GCP delete failed: {e}")
            return {"status": "error", "message": str(e)}
'''
            
    def run(self):
        """Run Week 5 cloud integration"""
        logger.info("Starting Week 5 cloud integration...")
        
        try:
            # Test cloud integrations
            aws_result = self.test_aws_integration()
            azure_result = self.test_azure_integration()
            gcp_result = self.test_gcp_integration()
            
            # Create cloud handler
            self.create_cloud_handler()
            
            # Save test results
            results = {
                "aws": aws_result,
                "azure": azure_result,
                "gcp": gcp_result,
                "timestamp": datetime.now().isoformat()
            }
            
            results_file = self.script_dir / 'reports' / 'cloud_integration_results.json'
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
                
            logger.info("Week 5 cloud integration completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Week 5 cloud integration failed: {e}")
            return False

if __name__ == "__main__":
    cloud_integration = Week5CloudIntegration()
    success = cloud_integration.run()
    sys.exit(0 if success else 1)
