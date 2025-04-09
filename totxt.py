"""Some utility that extract text from text-based docx, pdf etc... files.


functions:
    extract_doc_to_txt: Converts a text-based .docx file to a plain .txt file.
    extract_pdf_to_txt: Converts a text-based PDF file to a plain .txt file.
"""


__all__ = [
    'extract_doc_to_txt',
    'extract_pdf_to_txt',
]

from docx import Document
import PyPDF2


def extract_doc_to_txt(input_filepath, output_filepath):
    """Converts a text-based .docx file to a plain .txt file.

    Example usage:
    >>> extract_docx_to_txt('input.docx', 'output.txt')
    """
    if not input_filepath.lower().endswith('.docx'):
        raise ValueError("Only .docx files are supported (not .doc).")

    # Load the document
    doc = Document(input_filepath)
    text = "\n".join(para.text for para in doc.paragraphs)

    # Write to txt file
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def extract_pdf_to_txt(input_filepath, output_filepath):
    """Converts a text-based PDF file to a plain .txt file.

    Example usage:
    >>> extract_pdf_to_txt('input.pdf', 'output.txt')
    """
    if not input_filepath.lower().endswith('.pdf'):
        raise ValueError("Only .pdf files are supported.")

    with open(input_filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''  # handle None in case extract_text() returns None

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(text)