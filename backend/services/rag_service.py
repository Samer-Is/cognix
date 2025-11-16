"""
RAG (Retrieval Augmented Generation) Service
"""

import logging
from typing import Optional, Dict, Any, List
import boto3
from utils.config import settings
from services.document_processor import DocumentProcessor, SimpleVectorStore

logger = logging.getLogger(__name__)

# Global vector store instance
_vector_store = SimpleVectorStore()


class RAGService:
    """
    Service for handling document uploads and RAG functionality
    """
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.s3_bucket_uploads
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        user_id: int
    ) -> str:
        """
        Upload file to S3
        """
        
        s3_key = f"user_{user_id}/{filename}"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content
            )
            
            logger.info(f"File uploaded to S3: {s3_key}")
            return s3_key
            
        except Exception as e:
            logger.error(f"S3 upload error: {e}")
            raise
    
    async def delete_file(self, s3_key: str):
        """
        Delete file from S3
        """
        
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            logger.info(f"File deleted from S3: {s3_key}")
            
        except Exception as e:
            logger.error(f"S3 delete error: {e}")
            raise
    
    async def process_file(self, filename: str, file_content: bytes) -> Dict[str, Any]:
        """
        Process uploaded file for RAG
        1. Extract text content
        2. Chunk the content
        3. Store in vector database
        """
        
        logger.info(f"Processing file {filename} for RAG")
        
        # Process file based on type
        result = DocumentProcessor.process_file(filename, file_content)
        
        if "error" in result:
            logger.error(f"File processing error: {result['error']}")
            return result
        
        # Add chunks to vector store
        chunks = result.get("chunks", [])
        if chunks:
            _vector_store.add_documents(chunks)
            logger.info(f"Added {len(chunks)} chunks to vector store")
        
        return {
            "status": "success",
            "chunks_processed": len(chunks),
            "file_type": result.get("file_type"),
            "metadata": {
                k: v for k, v in result.items() 
                if k not in ["chunks", "error"]
            }
        }
    
    async def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks
        """
        results = _vector_store.simple_search(query, top_k=top_k)
        logger.info(f"Found {len(results)} relevant chunks for query: {query[:50]}")
        return results
    
    def get_vector_store_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store
        """
        documents = _vector_store.get_all_documents()
        return {
            "total_documents": len(documents),
            "document_types": list(set(doc.get("type", "unknown") for doc in documents))
        }
