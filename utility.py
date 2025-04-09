"""Utilities that converting file netween different format, using ffmepg.

functions:
    convert_audio: Converts an audio file to another format and reduces the file size by adjusting the bitrate.
    convert_video: Converts a video file to another format and adjusts the resolution and bitrate.
    convert_image: Converts an image file to another format and compress the image quality.
    get_file_size(filepath): Return the file size as a readable string like '12.56KB', '1.34MB', as well as number of bytes.
"""

__all__ = [
    'convert_audio',
    'convert_video',
    'convert_image',
    'convert_doc_to_txt',
    'convert_pdf_to_txt',
    'get_file_size',
]

from pydub import AudioSegment
from PIL import Image
import subprocess
import os

def convert_audio(input_filepath, output_filepath, *, bitrate="160k", print_info=False):
    """Converts an audio file to another format and reduces the file size by adjusting the bitrate.

    Example usage:
    >>> convert_audio('input.mp3', 'output.mp3', bitrate='32k')    

    Args:
        input_filepath (str): The path to the input audio file.
        output_filepath (str): The path to save the output audio file.
        output_format (str): The desired output format (default is "mp3").
        bitrate (str): The bitrate of output audio, high: 256k, mid: 160k, low: 96k.
        print_info (bool): print the converted filename, size, and size redunction.
    """
    # Get output format from the output file path
    output_format = os.path.splitext(output_filepath)[1][1:].lower()  # e.g., ".MP3" -> "mp3"
    if not output_format:
        raise ValueError("Output file must have an extension to determine the format.")
    
    audio = AudioSegment.from_file(input_filepath)
    audio.export(output_filepath, format=output_format, bitrate=bitrate)

    if print_info:
        size0_str, size0 = get_file_size(input_filepath)
        size1_str, size1 = get_file_size(output_filepath)
        print(
            f'convert: "{os.path.basename(input_filepath)}" ({size0_str}) -> ' +
            f'"{os.path.basename(output_filepath)}" ({size1_str}), {size1/size0*100:.2f}% of original size.'
        )


def convert_video(input_filepath, output_filepath, *, resolution="1280x720", bitrate="1000k", print_info=False):
    """Converts a video file to another format and adjusts the resolution and bitrate.

    Example usage:
    >>> convert_video('input.mp4', 'output.mp4', resolution='640x480', bitrate='256k')

    Args:
        input_filepath (str): The path to the input video file.
        output_filepath (str): The path to save the output video file.
        resolution (str): The desired resolution high: 1920x1080, mid: 1280x720, low: 640x480.
        bitrate (str): The bitrate of the output video, high: 3000k, mid: 1000k, low: 500k.
        print_info (bool): print the converted filename, size, and size redunction.
    """


    # Get output format from the output file path
    output_format = os.path.splitext(output_filepath)[1][1:].lower()  # e.g., ".MP4" -> "mp4"
    if not output_format:
        raise ValueError("Output file must have an extension to determine the format.")
    
    # Construct the ffmpeg command
    command = [
        "ffmpeg",
        "-y",  # force overwrite
        "-i", input_filepath,
        "-s", resolution,
        "-b:v", bitrate,
        output_filepath
    ]
    
    # Run the command to convert the video
    subprocess.run(command, check=True)

    if print_info:
        size0_str, size0 = get_file_size(input_filepath)
        size1_str, size1 = get_file_size(output_filepath)
        print(
            f'convert: "{os.path.basename(input_filepath)}" ({size0_str}) -> ' +
            f'"{os.path.basename(output_filepath)}" ({size1_str}), {size1/size0*100:.2f}% of original size.'
        )

from pillow_heif import register_heif_opener
register_heif_opener()
def convert_image(input_filepath, output_filepath, *, quality=85, suppres_warn=False, print_info=False):
    """Converts an image file to another format and compress the image quality.

    Example usage:
    >>> convert_image('input.png', 'output.jpg', format='JPEG', quality=90)

    Args:
        input_filepath (str): The path to the input image file.
        output_filepath (str): The path to save the output image file.
        format (str): The desired output image format (e.g., 'JPEG', 'PNG', 'BMP').
        quality (int): 0 to 100, 0 the quality of `image.save` function.
        suppres_warn (bool): supress the warning message printed.
        print_info (bool): print the converted filename, size, and size redunction.
    """
    # Open the input image
    image = Image.open(input_filepath)
    
    # Get output format from the output file name
    output_format = os.path.splitext(output_filepath)[1][1:].lower()  # e.g., ".jpg" -> "JPG"
    if not output_format:
        raise ValueError("Output file must have an extension to determine the format.")
    if output_format == 'jpg':
        output_format = 'jpeg'
    elif output_format in ['heic', 'heif']:
        output_format = 'heif'

    # Convert and save the image, if the transprancy is not support, conver image to RGB first
    try:
        image.save(output_filepath, format=output_format, quality=quality)
    except OSError as e:
        if 'cannot write mode RGBA' in str(e):
            if not suppres_warn:
                print('Warning: cannot write mode RGBA, so the transparency is wiped off in order to continue.')
            image = image.convert('RGB')
            image.save(output_filepath, format=output_format, quality=quality)

    if print_info:
        size0_str, size0 = get_file_size(input_filepath)
        size1_str, size1 = get_file_size(output_filepath)
        print(
            f'convert: "{os.path.basename(input_filepath)}" ({size0_str}) -> ' +
            f'"{os.path.basename(output_filepath)}" ({size1_str}), {size1/size0*100:.2f}% of original size.'
        )

def get_file_size(filepath):
    """Return the file size as a readable string like '12.56KB', '1.34MB', as well as number of bytes.
    
    Example usage:
    >>> get_readable_file_size("video.mkv")
    OUTPUT:
    | '284.88 MB', 298716659
    """
    size_bytes = os.path.getsize(filepath)
    if size_bytes == 0:
        return "0B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    value = size_bytes
    while value >= 1024 and i < len(units) - 1:
        value /= 1024.0
        i += 1
    return f"{value:.2f} {units[i]}", size_bytes


