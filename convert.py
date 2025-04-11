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
    'get_file_size',
]

from pydub import AudioSegment
from PIL import Image
import subprocess
import os

from pathkit import get_file_size


def print_conversion_info(input_filepath, output_filepath):
    size0_str, size0 = get_file_size(input_filepath)
    size1_str, size1 = get_file_size(output_filepath)
    print(
        f'convert: "{os.path.basename(input_filepath)}" ({size0_str}) -> ' +
        f'"{os.path.basename(output_filepath)}" ({size1_str}), {size1/size0*100:.2f}% of original size.'
    )

def convert_audio(input_filepath, output_filepath, *, bitrate="160k", print_info=False):
    """Converts an audio file to another format and reduces the file size by adjusting the bitrate.
    (Generate by AI)
    
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
        print_conversion_info()

def convert_video(input_filepath, output_filepath, *, resolution="1280x720", bitrate="1000k", print_info=False):
    """Converts a video file to another format and adjusts the resolution and bitrate.
    (Generate by AI)
    
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
        print_conversion_info()



from pillow_heif import register_heif_opener
register_heif_opener()
def convert_image(input_filepath, output_filepath, *, 
                  quality=85, keep_metadata=False, suppress_warn=False, print_info=False):
    """
    Convert image format while optionally keeping metadata using exiftool.

    Args:
        input_filepath (str): Source image.
        output_filepath (str): Destination image.
        quality (int): Compression quality for JPEG/WebP.
        keep_metadata (bool): keep metadata like gps location, camera parameters.
        suppress_warn (bool): Suppress Pillow warnings.
        print_info (bool): Show file size comparison.
    """
    image = Image.open(input_filepath)

    output_format = os.path.splitext(output_filepath)[1][1:].lower()
    if not output_format:
        raise ValueError("Output file must have an extension.")
    if output_format == 'jpg':
        output_format = 'jpeg'

    try:
        image.save(output_filepath, format=output_format, quality=quality)
    except OSError as e:
        if 'cannot write mode RGBA' in str(e):
            if not suppress_warn:
                print('Warning: RGBA mode not supported; converting to RGB.')
            image = image.convert('RGB')
            image.save(output_filepath, format=output_format, quality=quality)

    # Use exiftool to copy metadata
    if keep_metadata:
        try:
            subprocess.run([
                'exiftool',
                '-overwrite_original',
                f'-TagsFromFile={input_filepath}',
                output_filepath
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            if not suppress_warn:
                print("ExifTool is not installed or not in PATH. Metadata will not be copied.")
        except subprocess.CalledProcessError:
            if not suppress_warn:
                print("ExifTool failed to copy metadata.")

    if print_info:
        print_conversion_info()
