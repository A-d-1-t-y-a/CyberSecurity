"""
Cloud Handler for Memory Forensics Framework
Handles cloud memory dumps from AWS, Azure, and GCP
"""

import os
import tempfile
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import boto3
from azure.storage.blob import BlobServiceClient
from google.cloud import storage

class CloudHandler:
    """
    Handler for cloud memory dumps
    Supports AWS, Azure, and GCP cloud providers
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp(prefix="cloud_dumps_")
        
        # Initialize cloud clients
        self.aws_client = None
        self.azure_client = None
        self.gcp_client = None
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize cloud service clients"""
        try:
            # AWS S3 client
            self.aws_client = boto3.client('s3')
            self.logger.info("AWS S3 client initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize AWS client: {e}")
        
        try:
            # Azure Blob client
            connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            if connection_string:
                self.azure_client = BlobServiceClient.from_connection_string(connection_string)
                self.logger.info("Azure Blob client initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Azure client: {e}")
        
        try:
            # GCP Storage client
            self.gcp_client = storage.Client()
            self.logger.info("GCP Storage client initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize GCP client: {e}")
    
    def download_dump(self, 
                     dump_path: str, 
                     cloud_source: str,
                     **kwargs) -> str:
        """
        Download memory dump from cloud storage
        
        Args:
            dump_path: Path to dump in cloud storage
            cloud_source: Cloud provider (aws, azure, gcp)
            **kwargs: Additional parameters for cloud download
            
        Returns:
            Local path to downloaded dump
        """
        self.logger.info(f"Downloading dump from {cloud_source}: {dump_path}")
        
        if cloud_source.lower() == "aws":
            return self._download_from_aws(dump_path, **kwargs)
        elif cloud_source.lower() == "azure":
            return self._download_from_azure(dump_path, **kwargs)
        elif cloud_source.lower() == "gcp":
            return self._download_from_gcp(dump_path, **kwargs)
        else:
            raise ValueError(f"Unsupported cloud source: {cloud_source}")
    
    def _download_from_aws(self, 
                          dump_path: str, 
                          bucket: str,
                          **kwargs) -> str:
        """Download dump from AWS S3"""
        if not self.aws_client:
            raise RuntimeError("AWS client not initialized")
        
        # Parse S3 path (bucket/key)
        if '/' in dump_path:
            bucket, key = dump_path.split('/', 1)
        else:
            key = dump_path
        
        # Local file path
        local_path = os.path.join(self.temp_dir, os.path.basename(key))
        
        try:
            self.aws_client.download_file(bucket, key, local_path)
            self.logger.info(f"Downloaded from S3: {bucket}/{key} -> {local_path}")
            return local_path
        except Exception as e:
            self.logger.error(f"Failed to download from S3: {e}")
            raise
    
    def _download_from_azure(self, 
                            dump_path: str,
                            container: str,
                            **kwargs) -> str:
        """Download dump from Azure Blob Storage"""
        if not self.azure_client:
            raise RuntimeError("Azure client not initialized")
        
        # Parse Azure path (container/blob)
        if '/' in dump_path:
            container, blob_name = dump_path.split('/', 1)
        else:
            blob_name = dump_path
        
        # Local file path
        local_path = os.path.join(self.temp_dir, os.path.basename(blob_name))
        
        try:
            blob_client = self.azure_client.get_blob_client(
                container=container, blob=blob_name
            )
            
            with open(local_path, 'wb') as f:
                download_stream = blob_client.download_blob()
                f.write(download_stream.readall())
            
            self.logger.info(f"Downloaded from Azure: {container}/{blob_name} -> {local_path}")
            return local_path
        except Exception as e:
            self.logger.error(f"Failed to download from Azure: {e}")
            raise
    
    def _download_from_gcp(self, 
                          dump_path: str,
                          bucket: str,
                          **kwargs) -> str:
        """Download dump from GCP Cloud Storage"""
        if not self.gcp_client:
            raise RuntimeError("GCP client not initialized")
        
        # Parse GCP path (bucket/blob)
        if '/' in dump_path:
            bucket, blob_name = dump_path.split('/', 1)
        else:
            blob_name = dump_path
        
        # Local file path
        local_path = os.path.join(self.temp_dir, os.path.basename(blob_name))
        
        try:
            bucket_obj = self.gcp_client.bucket(bucket)
            blob = bucket_obj.blob(blob_name)
            
            blob.download_to_filename(local_path)
            self.logger.info(f"Downloaded from GCP: {bucket}/{blob_name} -> {local_path}")
            return local_path
        except Exception as e:
            self.logger.error(f"Failed to download from GCP: {e}")
            raise
    
    def upload_results(self, 
                      results_path: str, 
                      cloud_destination: str,
                      **kwargs) -> bool:
        """
        Upload analysis results to cloud storage
        
        Args:
            results_path: Path to results file
            cloud_destination: Cloud destination (provider://bucket/path)
            **kwargs: Additional parameters
            
        Returns:
            Success status
        """
        self.logger.info(f"Uploading results to: {cloud_destination}")
        
        # Parse destination
        if '://' in cloud_destination:
            provider, path = cloud_destination.split('://', 1)
        else:
            provider = "aws"  # Default
            path = cloud_destination
        
        try:
            if provider.lower() == "aws":
                return self._upload_to_aws(results_path, path, **kwargs)
            elif provider.lower() == "azure":
                return self._upload_to_azure(results_path, path, **kwargs)
            elif provider.lower() == "gcp":
                return self._upload_to_gcp(results_path, path, **kwargs)
            else:
                raise ValueError(f"Unsupported cloud provider: {provider}")
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            return False
    
    def _upload_to_aws(self, 
                      file_path: str, 
                      s3_path: str,
                      **kwargs) -> bool:
        """Upload to AWS S3"""
        if not self.aws_client:
            raise RuntimeError("AWS client not initialized")
        
        bucket, key = s3_path.split('/', 1) if '/' in s3_path else (s3_path, os.path.basename(file_path))
        
        try:
            self.aws_client.upload_file(file_path, bucket, key)
            self.logger.info(f"Uploaded to S3: {file_path} -> {bucket}/{key}")
            return True
        except Exception as e:
            self.logger.error(f"S3 upload failed: {e}")
            return False
    
    def _upload_to_azure(self, 
                        file_path: str, 
                        azure_path: str,
                        **kwargs) -> bool:
        """Upload to Azure Blob Storage"""
        if not self.azure_client:
            raise RuntimeError("Azure client not initialized")
        
        container, blob_name = azure_path.split('/', 1) if '/' in azure_path else (azure_path, os.path.basename(file_path))
        
        try:
            blob_client = self.azure_client.get_blob_client(
                container=container, blob=blob_name
            )
            
            with open(file_path, 'rb') as f:
                blob_client.upload_blob(f, overwrite=True)
            
            self.logger.info(f"Uploaded to Azure: {file_path} -> {container}/{blob_name}")
            return True
        except Exception as e:
            self.logger.error(f"Azure upload failed: {e}")
            return False
    
    def _upload_to_gcp(self, 
                      file_path: str, 
                      gcp_path: str,
                      **kwargs) -> bool:
        """Upload to GCP Cloud Storage"""
        if not self.gcp_client:
            raise RuntimeError("GCP client not initialized")
        
        bucket, blob_name = gcp_path.split('/', 1) if '/' in gcp_path else (gcp_path, os.path.basename(file_path))
        
        try:
            bucket_obj = self.gcp_client.bucket(bucket)
            blob = bucket_obj.blob(blob_name)
            
            blob.upload_from_filename(file_path)
            self.logger.info(f"Uploaded to GCP: {file_path} -> {bucket}/{blob_name}")
            return True
        except Exception as e:
            self.logger.error(f"GCP upload failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.logger.info("Cleaned up temporary files")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup temp directory: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get cloud handler information"""
        return {
            "name": "Cloud Handler",
            "version": "1.0.0",
            "temp_dir": self.temp_dir,
            "aws_available": self.aws_client is not None,
            "azure_available": self.azure_client is not None,
            "gcp_available": self.gcp_client is not None
        }
    
    def __del__(self):
        """Destructor to cleanup temporary files"""
        self.cleanup()
