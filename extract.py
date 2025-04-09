"""Some utility that extract text, images from text-based docx, pdf etc... files.


functions:
    extract_text_from_doc: Extract text from text-based .docx file, optionally to .txt file.
    extract_text_from_pdf: Extract text from text-based .pdf file, optionally to .txt file.
    extract_images_from_doc:
    extract_images_from_pdf:
"""


__all__ = [
    'extract_text_from_doc',
    'extract_text_from_pdf',
    'extract_images_from_doc',
    'extract_images_from_pdf',
]

from docx import Document
import PyPDF2
from PIL import Image, ImageChops
from io import BytesIO
import zipfile
import fitz

def extract_text_from_doc(input_filepath, output_filepath='') -> str:
    """Extract text from text-based .docx file, optionally to .txt file.
    (Generate by AI)
    
    Example usage:
    >>> text_from_doc = extract_text_from_doc('input.docx', 'output.txt')

    Args:
        input_filepath (string): filepath of .docx file
        output_filepath (string): file path of the .txt file. Empty string for not saving it.

    Returns:
        extracted_text (string): the extracted text.
    """
    if not input_filepath.lower().endswith('.docx'):
        raise ValueError("Only .docx files are supported (not .doc).")

    # Load the document
    doc = Document(input_filepath)
    text = "\n".join(para.text for para in doc.paragraphs)

    if output_filepath != '':
        # Write to txt file
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    return text

def extract_text_from_pdf(input_filepath, output_filepath='') -> str:
    """Extract text from text-based .pdf file, optionally to .txt file.
    (Generate by AI)
    
    Example usage:
    >>> text_from_pdf = extract_text_from_pdf('input.pdf', 'output.txt')

    Args:
        input_filepath (string): filepath of .docx file
        output_filepath (string or None): file path of the .txt file. None for not saving it.

    Returns:
        extracted_text (string): the extracted text.
    """
    if not input_filepath.lower().endswith('.pdf'):
        raise ValueError("Only .pdf files are supported.")

    with open(input_filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''  # handle None in case extract_text() returns None

    if output_filepath != '':
        # Write to txt file
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    return text


def extract_images_from_doc(input_filepath) -> list:
    """extract images from a .docx file and return as a list of images.
    (Generate by AI)
    
    Example usage:
    >>> images = extract_images_from_doc('input.pdf')
    >>> first_image = images[0]
    >>> # user can manually save it
    >>> first_image.save('output.png', format='.jpg', quality=85)
    """
    if not input_filepath.lower().endswith('.docx'):
        raise ValueError("Only .docx files are supported.")

    images = []
    with zipfile.ZipFile(input_filepath, 'r') as docx_zip:
        for file_info in docx_zip.infolist():
            if file_info.filename.startswith("word/media/") and file_info.filename.lower().endswith(('.png', '.jpeg', '.jpg', '.bmp', '.gif')):
                with docx_zip.open(file_info) as img_file:
                    image = Image.open(BytesIO(img_file.read()))
                    images.append(image.copy())  # Copy to close underlying file later
                    image.close()

    return images

    

def extract_images_from_pdf(input_filepath) -> list:
    """extract images from a .pdf file and return as a list of images.
    (Generate by AI)

    Example usage:
    >>> images = extract_images_from_pdf('input.pdf')
    >>> first_image = images[0]
    >>> # user can manually save it
    >>> first_image.save('output.png', format='.jpg', quality=85)
    """
    if not input_filepath.lower().endswith('.pdf'):
        raise ValueError("Only .pdf files are supported.")

    images = []
    doc = fitz.open(input_filepath)

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes)).convert("RGB")  # Ensure 3 channels
            
            # Create a pure black image of same size
            black_bg = Image.new("RGB", image.size, (0, 0, 0))
            
            # Compare: is the image all black?
            diff = ImageChops.difference(image, black_bg)
            if diff.getbbox() is None:
                continue  # Skip pure black image

            images.append(image.copy())
            image.close()

    return images
