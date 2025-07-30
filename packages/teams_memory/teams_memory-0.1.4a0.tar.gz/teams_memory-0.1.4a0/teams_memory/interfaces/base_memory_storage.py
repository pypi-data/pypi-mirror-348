"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from teams_memory.interfaces.types import (
    BaseMemoryInput,
    Memory,
    TextEmbedding,
)


class BaseMemoryStorage(ABC):
    """Base class for the storage component.

    This class defines the interface for persistent storage of memories and messages.
    It handles the low-level storage operations including storing, retrieving, updating,
    and searching memories and messages with their associated embeddings.
    """

    default_limit = 10

    @abstractmethod
    async def store_memory(
        self,
        memory: BaseMemoryInput,
        *,
        embedding_vectors: List[TextEmbedding],
    ) -> str | None:
        """Store a memory with its embedding vectors in the storage system.

        Args:
            memory (BaseMemoryInput): The Memory object to store, containing the memory content and metadata
            embedding_vectors (List[TextEmbedding]): List of TextEmbedding objects containing both vectors
                            and their source text for semantic search

        Returns:
            str | None: The ID of the stored memory if successful, None otherwise
        """
        pass

    @abstractmethod
    async def update_memory(
        self,
        memory_id: str,
        updated_memory: str,
        *,
        embedding_vectors: List[TextEmbedding],
    ) -> None:
        """Update an existing memory with new content and embeddings.

        Args:
            memory_id (str): ID of the memory to update
            updated_memory (str): New content for the memory
            embedding_vectors (List[TextEmbedding]): New embedding vectors for the updated content

        Raises:
            MemoryNotFoundError: If the specified memory_id doesn't exist
        """
        pass

    @abstractmethod
    async def get_memories(
        self, *, memory_ids: Optional[List[str]] = None, user_id: Optional[str] = None
    ) -> List[Memory]:
        """Retrieve memories by IDs or user.

        At least one parameter must be provided.

        Args:
            memory_ids (Optional[List[str]]): Optional list of specific memory IDs to retrieve
            user_id (Optional[str]): Optional user ID to retrieve all memories for

        Returns:
            List[Memory]: List of memory objects matching the criteria

        Raises:
            ValueError: If neither memory_ids nor user_id is provided
        """
        pass

    @abstractmethod
    async def get_memory(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a memory by its ID.

        Args:
            memory_id (str): ID of the memory to retrieve

        Returns:
            Optional[Memory]: Memory object if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_attributed_memories(self, message_ids: List[str]) -> List[Memory]:
        """Retrieve all memories from storage that are attributed to the provided message IDs.

        Args:
            message_ids (List[str]): List of message IDs to filter memories by source

        Returns:
            List[Memory]: List of memory objects ordered by creation date (newest first)
        """
        pass

    @abstractmethod
    async def search_memories(
        self,
        *,
        user_id: Optional[str],
        text_embedding: Optional[TextEmbedding] = None,
        topics: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> List[Memory]:
        """Search memories using semantic similarity and/or topics.

        Performs semantic search using embedding vectors and/or filters by topics.
        One of text_embedding or topics must be provided.

        Args:
            user_id (Optional[str]): Filter memories by specific user ID. If None, search across all users
            text_embedding (Optional[TextEmbedding]): Vector embedding for semantic similarity search
            topics (Optional[List[Topic]]): List of topics to filter memories by
            limit (Optional[int]): Maximum number of memories to return. Defaults to default_limit if None

        Returns:
            List[Memory]: List of memories matching the criteria, ordered by relevance

        Raises:
            ValueError: If neither text_embedding nor topics is provided
        """
        pass

    @abstractmethod
    async def delete_memories(
        self, *, user_id: Optional[str] = None, memory_ids: Optional[List[str]] = None
    ) -> None:
        """Remove memories from storage.

        At least one parameter must be provided.

        Args:
            user_id (Optional[str]): Optional user ID to remove all memories for
            memory_ids (Optional[List[str]]): Optional list of specific memory IDs to remove

        Raises:
            ValueError: If neither memory_ids nor user_id is provided
        """
        pass
