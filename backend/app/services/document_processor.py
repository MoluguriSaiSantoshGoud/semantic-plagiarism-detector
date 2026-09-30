from typing import List, Dict, Optional
from pathlib import Path
import re
from pypdf import PdfReader
from docx import Document


class DocumentProcessor:
    """Process documents and extract text with metadata."""
    
    def __init__(self):
        pass
    
    def extract_text(self, file_path: str, file_type: str) -> Dict:
        """Extract text from document based on file type."""
        file_type = file_type.lower()
        
        if file_type == "pdf":
            return self._extract_pdf(file_path)
        elif file_type == "docx":
            return self._extract_docx(file_path)
        elif file_type == "txt":
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _extract_pdf(self, file_path: str) -> Dict:
        """Extract text from PDF file."""
        try:
            reader = PdfReader(file_path)
            full_text = ""
            pages_text = []
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    pages_text.append({
                        "page_number": page_num + 1,
                        "text": page_text
                    })
                    full_text += page_text + "\n\n"
            
            if not full_text.strip():
                return {
                    "error": "No extractable text found in PDF. OCR may be required for scanned documents.",
                    "full_text": "",
                    "page_count": len(reader.pages),
                    "word_count": 0
                }
            
            paragraphs = self._split_into_paragraphs(full_text)
            chunks = self._create_chunks(paragraphs)
            
            return {
                "full_text": self._clean_text(full_text),
                "page_count": len(reader.pages),
                "word_count": len(self._clean_text(full_text).split()),
                "paragraphs": paragraphs,
                "chunks": chunks
            }
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
    
    def _extract_docx(self, file_path: str) -> Dict:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            paragraphs_text = []
            full_text = ""
            
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs_text.append(para.text)
                    full_text += para.text + "\n\n"
            
            if not full_text.strip():
                return {
                    "error": "No text found in DOCX file.",
                    "full_text": "",
                    "page_count": 0,
                    "word_count": 0
                }
            
            cleaned_paragraphs = [self._clean_text(p) for p in paragraphs_text if self._clean_text(p)]
            chunks = self._create_chunks(cleaned_paragraphs)
            
            return {
                "full_text": self._clean_text(full_text),
                "page_count": len(doc.sections),
                "word_count": len(self._clean_text(full_text).split()),
                "paragraphs": cleaned_paragraphs,
                "chunks": chunks
            }
        except Exception as e:
            raise Exception(f"DOCX extraction failed: {str(e)}")
    
    def _extract_txt(self, file_path: str) -> Dict:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text.strip():
                return {
                    "error": "No text found in TXT file.",
                    "full_text": "",
                    "page_count": 0,
                    "word_count": 0
                }
            
            cleaned_text = self._clean_text(text)
            paragraphs = self._split_into_paragraphs(cleaned_text)
            chunks = self._create_chunks(paragraphs)
            
            return {
                "full_text": cleaned_text,
                "page_count": 1,
                "word_count": len(cleaned_text.split()),
                "paragraphs": paragraphs,
                "chunks": chunks
            }
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    text = f.read()
                cleaned_text = self._clean_text(text)
                paragraphs = self._split_into_paragraphs(cleaned_text)
                chunks = self._create_chunks(paragraphs)
                
                return {
                    "full_text": cleaned_text,
                    "page_count": 1,
                    "word_count": len(cleaned_text.split()),
                    "paragraphs": paragraphs,
                    "chunks": chunks
                }
            except Exception as e:
                raise Exception(f"TXT extraction failed: {str(e)}")
        except Exception as e:
            raise Exception(f"TXT extraction failed: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove repeated blank lines
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Normalize quotation marks
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove control characters but keep meaningful punctuation
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip() and len(p.split()) > 2]
    
    def _create_chunks(self, paragraphs: List[str], chunk_size: int = 150, overlap: int = 30) -> List[Dict]:
        """Create chunks from paragraphs with overlap."""
        chunks = []
        chunk_id = 0
        
        for para_idx, paragraph in enumerate(paragraphs):
            words = paragraph.split()
            
            if len(words) <= chunk_size:
                chunks.append({
                    "chunk_id": chunk_id,
                    "chunk_index": chunk_id,
                    "paragraph_index": para_idx,
                    "page_number": 1,
                    "text": paragraph,
                    "word_count": len(words)
                })
                chunk_id += 1
            else:
                # Split large paragraphs into overlapping chunks
                for i in range(0, len(words), chunk_size - overlap):
                    chunk_words = words[i:i + chunk_size]
                    if len(chunk_words) > 2:  # Avoid tiny chunks
                        chunks.append({
                            "chunk_id": chunk_id,
                            "chunk_index": chunk_id,
                            "paragraph_index": para_idx,
                            "page_number": 1,
                            "text": " ".join(chunk_words),
                            "word_count": len(chunk_words)
                        })
                        chunk_id += 1
        
        return chunks
    
    def process_text_input(self, text: str) -> Dict:
        """Process direct text input (not from file)."""
        if not text or not text.strip():
            return {
                "error": "Empty text provided.",
                "full_text": "",
                "page_count": 0,
                "word_count": 0
            }
        
        cleaned_text = self._clean_text(text)
        paragraphs = self._split_into_paragraphs(cleaned_text)
        chunks = self._create_chunks(paragraphs)
        
        return {
            "full_text": cleaned_text,
            "page_count": 1,
            "word_count": len(cleaned_text.split()),
            "paragraphs": paragraphs,
            "chunks": chunks
        }
