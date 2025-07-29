from abc import ABC, abstractmethod
import openai
import google.generativeai as genai
from typing import List, Union, Optional

class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""
    
    @abstractmethod
    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings for one or more texts.
        
        Args:
            texts: A single string or list of strings to embed.
        
        Returns:
            A list of embeddings, where each embedding is a list of floats.
        """
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """
        Return the dimension of the embeddings produced by this provider.
        
        Returns:
            The embedding dimension (e.g., 1536 for OpenAI text-embedding-3-small).
        """
        pass

class OpenAIEmbeddingProvider(EmbeddingProvider):
    """Embedding provider for OpenAI's embedding models."""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        """
        Initialize the OpenAI embedding provider.
        
        Args:
            api_key: OpenAI API key.
            model: Embedding model name (e.g., 'text-embedding-3-small').
        """
        self.client = openai.Client(api_key=api_key)
        self.model = model
        self._dimension = None  # Set after first embedding call
    
    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI's embedding model.
        
        Args:
            texts: A single string or list of strings to embed.
        
        Returns:
            A list of embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            embeddings = [data.embedding for data in response.data]
            
            # Set dimension on first call
            if self._dimension is None and embeddings:
                self._dimension = len(embeddings[0])
            
            return embeddings
        except Exception as e:
            raise Exception(f"OpenAI embedding error: {str(e)}")
    
    def get_dimension(self) -> int:
        """
        Return the embedding dimension.
        
        Returns:
            The dimension of the embeddings (e.g., 1536 for text-embedding-3-small).
        
        Raises:
            ValueError: If dimension is not yet known.
        """
        if self._dimension is None:
            # Generate a dummy embedding to get dimension
            dummy_embedding = self.embed("test")[0]
            self._dimension = len(dummy_embedding)
        return self._dimension

class GeminiEmbeddingProvider(EmbeddingProvider):
    """Embedding provider for Google's Gemini embedding models."""
    
    def __init__(self, api_key: str, model: str = "embedding-001"):
        """
        Initialize the Gemini embedding provider.
        
        Args:
            api_key: Google API key.
            model: Embedding model name (e.g., 'embedding-001').
        """
        genai.configure(api_key=api_key)
        self.model = f"models/{model}"
        self._dimension = 768  # Known dimension for embedding-001
    
    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Generate embeddings using Gemini's embedding model.
        
        Args:
            texts: A single string or list of strings to embed.
        
        Returns:
            A list of embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="RETRIEVAL_DOCUMENT"
                )
                embeddings.append(result["embedding"])
            return embeddings
        except Exception as e:
            raise Exception(f"Gemini embedding error: {str(e)}")
    
    def get_dimension(self) -> int:
        """
        Return the embedding dimension.
        
        Returns:
            The dimension of the embeddings (768 for embedding-001).
        """
        return self._dimension