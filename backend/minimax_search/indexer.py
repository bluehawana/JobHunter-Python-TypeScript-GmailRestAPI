"""
Document indexer for searching job applications, CVs, and cover letters.
"""

from pathlib import Path
from typing import Dict, List, Optional
import logging

from .models import Document

logger = logging.getLogger(__name__)


class DocumentIndexer:
    """Indexes and retrieves documents for search"""
    
    def __init__(self, base_paths: List[Path]):
        """
        Initialize document indexer.
        
        Args:
            base_paths: List of base paths to index
        """
        self.base_paths = [Path(p) for p in base_paths]
        self.index: Dict[str, Document] = {}
        
        logger.info(f"Initialized DocumentIndexer with {len(base_paths)} base paths")
    
    def build_index(self) -> None:
        """Build or rebuild document index"""
        # TODO: Implement index building
        raise NotImplementedError("Index building will be implemented in task 5.2")
    
    def get_documents(self, document_types: Optional[List[str]] = None) -> List[Document]:
        """
        Retrieve documents by type.
        
        Args:
            document_types: Optional list of document types to filter by
            
        Returns:
            List of documents matching the filter
        """
        # TODO: Implement document retrieval
        raise NotImplementedError("Document retrieval will be implemented in task 5.2")
    
    def update_document(self, file_path: Path) -> None:
        """
        Update index for a single document.
        
        Args:
            file_path: Path to document to update
        """
        # TODO: Implement document update
        raise NotImplementedError("Document update will be implemented in task 5.5")
    
    def extract_text(self, file_path: Path) -> str:
        """
        Extract text from LaTeX/PDF files.
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text content
        """
        # TODO: Implement text extraction
        raise NotImplementedError("Text extraction will be implemented in task 5.3")
