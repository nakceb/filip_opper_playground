from enum import Enum
from typing import List
import streamlit as st
import logging
import PyPDF2
import requests
import io
from typing import Optional, Tuple
from pathlib import Path


class InputType(Enum):
    PDF_READER_UPLOAD = "pdf_reader_upload"
    PDF_READER_DOWNLOAD = "pdf_reader_download"

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns a list of trigger type values for dropdown display"""
        return [key.value for key in cls]

    def __str__(self):
        return self.value

    @staticmethod
    def display():
        return st.selectbox(
            "Select Input",
            InputType.get_values(),
            format_func=str,
            index=None
        )

class PDFHandler:
    @staticmethod
    def read_pdf(file_obj) -> Tuple[str, int]:
        """
        Read a PDF file and return its text content and page count

        Args:
            file_obj: File object of the PDF

        Returns:
            Tuple containing the extracted text and number of pages
        """
        try:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file_obj)
            num_pages = len(pdf_reader.pages)

            # Extract text from all pages
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n\n"

            return text_content.strip(), num_pages

        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return "", 0

    @staticmethod
    def download_pdf(url: str) -> Optional[io.BytesIO]:
        """
        Download a PDF from a URL

        Args:
            url: URL of the PDF to download

        Returns:
            BytesIO object containing the PDF data or None if failed
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Check if content is PDF
            if 'application/pdf' not in response.headers.get('content-type', '').lower():
                st.error("The URL does not point to a PDF file")
                return None

            return io.BytesIO(response.content)

        except requests.exceptions.RequestException as e:
            st.error(f"Error downloading PDF: {str(e)}")
            return None


class Input:
    """ Input is the origin of data that comes in into the pipeline """
    def __init__(
            self,
            node_id: int,
    ):
        self.name = "Input"
        self.as_coroutine = False
        self.node_id = node_id
        self.pdf_handler = PDFHandler()
        self.text_content = None # This will store pdf content

    def call(self, _=None) -> str:
        if self.text_content is None:
            logging.warning("Failed to populate Input!")
        return self.text_content

    @staticmethod
    def display():
        st.selectbox(
            "Select Input",
            InputType.get_values(),
            format_func=str
        )

def display_download_pdf():
    pdf_handler = PDFHandler()
    st.header("Download PDF from URL")
    url = st.text_input("Enter PDF URL")

    if url and st.button("Download"):
        pdf_data = pdf_handler.download_pdf(url)

        if pdf_data:
            # Generate filename from URL
            filename = url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename = 'downloaded.pdf'

            # Read PDF content
            text_content, num_pages = pdf_handler.read_pdf(pdf_data)

            # Display PDF information
            st.success(f"Successfully downloaded PDF: {filename}")
            st.info(f"Number of pages: {num_pages}")

            # Show extracted text with copy option
            with st.expander("View extracted text"):
                st.text_area("PDF Content", text_content, height=300)

            return text_content
    return None

def display_uploaded_pdf():
    pdf_handler = PDFHandler()
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Create a unique filename
        file_path = Path(uploaded_file.name)

        # Read PDF content
        text_content, num_pages = pdf_handler.read_pdf(uploaded_file)

        # Display PDF information
        st.success(f"Successfully read PDF: {file_path.name}")
        st.info(f"Number of pages: {num_pages}")

        # Show extracted text with copy option
        with st.expander("View extracted text"):
            st.text_area("PDF Content", text_content, height=300)
        return text_content
    return None