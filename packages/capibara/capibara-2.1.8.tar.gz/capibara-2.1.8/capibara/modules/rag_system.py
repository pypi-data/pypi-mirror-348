from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
import torch
import jax
import jax.numpy as jnp
from flax import linen as nn
from flax.training import train_state
import optax

class TPUEmbeddingModel(nn.Module):
    """Modelo de embeddings optimizado para TPU."""
    embedding_dim: int = 768
    vocab_size: int = 30522
    
    @nn.compact
    def __call__(self, x):
        x = nn.Embed(self.vocab_size, self.embedding_dim)(x)
        x = nn.LayerNorm()(x)
        return x

class RAGSystem:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        device: str = "tpu" if jax.devices("tpu") else "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """
        Inicializa el sistema RAG con soporte TPU.
        
        Args:
            model_name: Nombre del modelo de embeddings a utilizar
            chunk_size: Tamaño de los chunks para dividir documentos
            chunk_overlap: Superposición entre chunks
            device: Dispositivo para ejecutar el modelo (tpu/cuda/cpu)
        """
        self.device = device
        
        if device == "tpu":
            # Inicializar modelo JAX/Flax para TPU
            self.embedding_model = TPUEmbeddingModel()
            self.params = self.embedding_model.init(jax.random.PRNGKey(0), jnp.ones((1, 512), dtype=jnp.int32))
            self.state = train_state.TrainState.create(
                apply_fn=self.embedding_model.apply,
                params=self.params,
                tx=optax.adam(1e-4)
            )
        else:
            # Usar modelo PyTorch para CPU/GPU
            self.embedding_model = SentenceTransformer(model_name, device=device)
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.vector_store = None
        
    def _encode_tpu(self, texts: List[str]) -> np.ndarray:
        """Codifica textos usando TPU."""
        # Tokenizar textos (implementación simplificada)
        tokens = np.array([[1] * 512 for _ in texts])  # Placeholder
        
        # Aplicar modelo en TPU
        embeddings = jax.jit(self.state.apply_fn)(self.state.params, tokens)
        return np.array(embeddings)
        
    def _encode_standard(self, texts: List[str]) -> np.ndarray:
        """Codifica textos usando CPU/GPU."""
        return self.embedding_model.encode(texts)
        
    def load_documents(self, directory: str) -> None:
        """
        Carga documentos de un directorio y los procesa.
        
        Args:
            directory: Ruta al directorio con los documentos
        """
        loader = DirectoryLoader(directory, glob="**/*.txt")
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        
        # Crear embeddings según el dispositivo
        if self.device == "tpu":
            embeddings = self._encode_tpu([doc.page_content for doc in texts])
        else:
            embeddings = self._encode_standard([doc.page_content for doc in texts])
            
        self.vector_store = FAISS.from_embeddings(
            embeddings,
            texts,
            self.embedding_model
        )
        
    def query(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Realiza una consulta al sistema RAG.
        
        Args:
            query: Texto de la consulta
            k: Número de documentos relevantes a recuperar
            
        Returns:
            Lista de documentos relevantes con sus metadatos
        """
        if self.vector_store is None:
            raise ValueError("El sistema RAG no ha sido inicializado con documentos")
            
        # Obtener documentos relevantes
        docs = self.vector_store.similarity_search(query, k=k)
        
        # Formatear resultados
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": doc.score if hasattr(doc, "score") else None
            })
            
        return results
        
    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Añade un nuevo documento al sistema RAG.
        
        Args:
            text: Contenido del documento
            metadata: Metadatos opcionales del documento
        """
        if metadata is None:
            metadata = {}
            
        # Dividir el texto en chunks
        chunks = self.text_splitter.split_text(text)
        
        # Crear embeddings según el dispositivo
        if self.device == "tpu":
            embeddings = self._encode_tpu(chunks)
        else:
            embeddings = self._encode_standard(chunks)
        
        # Añadir al vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_embeddings(
                embeddings,
                [{"page_content": chunk, "metadata": metadata} for chunk in chunks],
                self.embedding_model
            )
        else:
            self.vector_store.add_embeddings(
                embeddings,
                [{"page_content": chunk, "metadata": metadata} for chunk in chunks]
            ) 