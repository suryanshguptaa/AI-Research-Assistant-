import streamlit as st
import PyPDF2
import pdfplumber
from docx import Document as DocxDocument
from typing import Dict, Any
import tempfile
import os
from helpers.langchain_helper import LangChainHelper
from config.settings import SUPPORTED_FORMATS, MAX_FILE_SIZE  # ADD THIS LINE

# Rest of the class remains the same...



class DocumentProcessor:
    """Advanced document processing with multiple format support."""

    def __init__(self):
        self.langchain_helper = LangChainHelper()
        self.supported_formats = SUPPORTED_FORMATS
        self.max_file_size = MAX_FILE_SIZE * 1024 * 1024  # Convert to bytes

    def validate_file(self, uploaded_file) -> Dict[str, Any]:
        """Validate uploaded file format and size."""
        validation_result = {
            "valid": False,
            "message": "",
            "file_info": {}
        }

        if uploaded_file is None:
            validation_result["message"] = "No file uploaded."
            return validation_result

        # Check file size
        if uploaded_file.size > self.max_file_size:
            validation_result["message"] = f"File size exceeds {MAX_FILE_SIZE}MB limit."
            return validation_result

        # Check file format
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in self.supported_formats:
            validation_result["message"] = f"Unsupported format. Supported: {', '.join(self.supported_formats)}"
            return validation_result

        validation_result.update({
            "valid": True,
            "message": "File validation successful.",
            "file_info": {
                "name": uploaded_file.name,
                "size": uploaded_file.size,
                "type": file_extension
            }
        })

        return validation_result

    def extract_text_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF using multiple methods for robustness."""
        text = ""

        try:
            # Method 1: pdfplumber (preferred for complex layouts)
            with pdfplumber.open(uploaded_file) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n\n--- Page {page_num + 1} ---\n\n"
                            text += page_text
                    except Exception as e:
                        st.warning(f"Could not extract text from page {page_num + 1}: {e}")
                        continue

            # If pdfplumber fails, fallback to PyPDF2
            if not text.strip():
                uploaded_file.seek(0)  # Reset file pointer
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n\n--- Page {page_num + 1} ---\n\n"
                            text += page_text
                    except Exception as e:
                        st.warning(f"Fallback extraction failed for page {page_num + 1}: {e}")
                        continue

        except Exception as e:
            st.error(f"PDF extraction failed: {e}")
            return ""

        return text.strip()

    def extract_text_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX files."""
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # Extract text using python-docx
            doc = DocxDocument(tmp_file_path)
            text = ""

            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"

            # Clean up temporary file
            os.unlink(tmp_file_path)

            return text.strip()

        except Exception as e:
            st.error(f"DOCX extraction failed: {e}")
            return ""

    def extract_text_from_txt(self, uploaded_file) -> str:
        """Extract text from TXT files with encoding detection."""
        try:
            # Try UTF-8 first
            uploaded_file.seek(0)
            content = uploaded_file.read()

            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to other encodings
                for encoding in ['latin1', 'cp1252', 'iso-8859-1']:
                    try:
                        text = content.decode(encoding)
                        st.info(f"Text decoded using {encoding} encoding.")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise UnicodeDecodeError("Unable to decode file with any common encoding.")

            return text.strip()

        except Exception as e:
            st.error(f"TXT extraction failed: {e}")
            return ""

    def process_document(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded document and return extracted content."""
        # Validate file
        validation = self.validate_file(uploaded_file)
        if not validation["valid"]:
            return {
                "success": False,
                "message": validation["message"],
                "content": {}
            }

        file_info = validation["file_info"]
        file_type = file_info["type"]

        # Extract text based on file type
        text = ""
        if file_type == "pdf":
            text = self.extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            text = self.extract_text_from_docx(uploaded_file)
        elif file_type == "txt":
            text = self.extract_text_from_txt(uploaded_file)

        if not text.strip():
            return {
                "success": False,
                "message": "No text could be extracted from the document.",
                "content": {}
            }

        # Generate summary
        summary = self.langchain_helper.generate_summary(text)

        # Create document chunks
        chunks = self.langchain_helper.text_splitter.split_text(text)

        # Create metadata
        metadata = {
            "filename": file_info["name"],
            "file_size": file_info["size"],
            "file_type": file_type,
            "total_chunks": len(chunks),
            "word_count": len(text.split()),
            "char_count": len(text)
        }

        return {
            "success": True,
            "message": f"Successfully processed {file_info['name']}",
            "content": {
                "raw_text": text,
                "summary": summary,
                "chunks": chunks,
                "metadata": metadata
            }
        }
