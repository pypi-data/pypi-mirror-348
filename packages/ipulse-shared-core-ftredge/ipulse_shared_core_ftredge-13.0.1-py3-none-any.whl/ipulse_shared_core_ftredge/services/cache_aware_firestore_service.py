"""Base service with built-in cache awareness for Firestore operations."""

from typing import Dict, Any, List, Optional, TypeVar, Generic
from google.cloud import firestore
from pydantic import BaseModel
import logging
from ipulse_shared_core_ftredge.cache.shared_cache import SharedCache
from ipulse_shared_core_ftredge.services import BaseFirestoreService

T = TypeVar('T', bound=BaseModel)

class CacheAwareFirestoreService(BaseFirestoreService, Generic[T]):
    """
    Base service class that integrates caching with Firestore operations.
    This allows services to inherit cache-aware CRUD methods without reimplementing them.
    """

    def __init__(
        self,
        db: firestore.Client,
        collection_name: str,
        resource_type: str,
        logger: logging.Logger,
        document_cache: Optional[SharedCache] = None,
        collection_cache: Optional[SharedCache] = None,
        timeout: float = 15.0
    ):
        """
        Initialize the service with optional cache instances.

        Args:
            db: Firestore client
            collection_name: Firestore collection name
            resource_type: Resource type for error messages
            logger: Logger instance
            document_cache: Cache for individual documents (optional)
            collection_cache: Cache for collection-level queries (optional)
            timeout: Firestore operation timeout in seconds
        """
        super().__init__(
            db=db,
            collection_name=collection_name,
            resource_type=resource_type,
            logger=logger,
            timeout=timeout
        )
        self.document_cache = document_cache
        self.collection_cache = collection_cache

        # Log cache configuration
        if document_cache:
            self.logger.info(f"Document cache enabled for {resource_type}: {document_cache.name}")
        if collection_cache:
            self.logger.info(f"Collection cache enabled for {resource_type}: {collection_cache.name}")

    async def create_document(self, doc_id: str, data: T, creator_uid: str) -> Dict[str, Any]:
        """Create a document and invalidate relevant caches."""
        result = await super().create_document(doc_id, data, creator_uid)

        # Invalidate document cache if it exists
        self._invalidate_document_cache(doc_id)

        # Invalidate collection cache if it exists
        self._invalidate_collection_cache()

        return result

    async def update_document(self, doc_id: str, update_data: Dict[str, Any], updater_uid: str) -> Dict[str, Any]:
        """Update a document and invalidate relevant caches."""
        result = await super().update_document(doc_id, update_data, updater_uid)

        # Invalidate document cache if it exists
        self._invalidate_document_cache(doc_id)

        # Invalidate collection cache if it exists
        self._invalidate_collection_cache()

        return result

    async def delete_document(self, doc_id: str, deleter_uid: Optional[str] = None) -> None:
        """Delete a document and invalidate relevant caches."""
        # Invalidate caches before deletion to handle potential failures
        self._invalidate_document_cache(doc_id)
        self._invalidate_collection_cache()

        # Delete the document
        await super().delete_document(doc_id)

    async def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Get a document by ID with caching if available.

        Args:
            doc_id: The document ID to fetch

        Returns:
            The document data
        """
        # Check document cache first if available
        if self.document_cache:
            cached_data = self.document_cache.get(doc_id)
            if cached_data is not None:
                self.logger.debug(f"Cache hit for document {doc_id}")
                return cached_data

        # Cache miss or no cache configured, fetch from Firestore
        doc_data = await super().get_document(doc_id)

        # Store in cache if available
        if self.document_cache and doc_data:
            # Make sure ID is included in the cached data
            if 'id' not in doc_data:
                doc_data['id'] = doc_id
            self.document_cache.set(doc_id, doc_data)
            self.logger.debug(f"Cached document {doc_id}")

        return doc_data

    async def get_all_documents(self, cache_key: str = "all_documents") -> List[Dict[str, Any]]:
        """
        Get all documents in the collection with caching.

        Args:
            cache_key: The key to use for caching the full collection

        Returns:
            List of all documents in the collection
        """
        # Check collection cache first if available
        if self.collection_cache:
            cached_data = self.collection_cache.get(cache_key)
            if cached_data is not None:
                self.logger.debug(f"Cache hit for collection query: {cache_key}")
                return cached_data

        # Cache miss or no cache configured, fetch from Firestore
        query = self.db.collection(self.collection_name).stream(timeout=self.timeout)
        documents = []

        for doc in query:
            doc_data = doc.to_dict()

            # Make sure ID is included in the data
            if 'id' not in doc_data:
                doc_data['id'] = doc.id

            # Also update the document cache if configured
            if self.document_cache:
                self.document_cache.set(doc.id, doc_data)

            documents.append(doc_data)

        # Store in collection cache if available
        if self.collection_cache:
            self.collection_cache.set(cache_key, documents)
            self.logger.debug(f"Cached collection query result: {cache_key} with {len(documents)} documents")

        return documents

    def _invalidate_document_cache(self, doc_id: str) -> None:
        """Invalidate the document cache for a specific document ID."""
        if self.document_cache:
            self.document_cache.invalidate(doc_id)
            self.logger.debug(f"Invalidated document cache for {doc_id}")

    def _invalidate_collection_cache(self, cache_key: str = "all_documents") -> None:
        """Invalidate the collection cache."""
        if self.collection_cache:
            # For single key collection cache
            self.collection_cache.invalidate(cache_key)
            self.logger.debug(f"Invalidated collection cache: {cache_key}")
