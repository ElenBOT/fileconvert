"""The file format convertor tool for image, video, audio. Using ffmpeg.

User need to download ffmpeg and other related module first.

filepath kits:
    get_filepath: Pop up a dialog to browse a file path (or save path) then return it.
    get_filepaths: Pop up a dialog to browse and select multiple files and returned as list.
    get_folderpath: Pop up a dialog to browse a folder path then return it.
    get_filepaths_under: Return file paths recursively from the given folder, can be filter by filename.
    replace_ext: Return a filepath with its file extension modified.

convertor tool:
    convert_audio: Converts an audio file to another format and reduces the file size by adjusting the bitrate.
    convert_video: Converts a video file to another format and adjusts the resolution and bitrate.
    convert_image: Converts an image file to another format and compress the image quality.
    get_file_size(filepath): Return the file size as a readable string like '12.56KB', '1.34MB', as well as number of bytes.


Example usage:
>>> from fileconvert import *
>>> 
>>> ## convert an (image, audio, video) to another format
>>> path0 = get_filepath()
>>> path1 = get_filepath(savefile=True)
>>> convert_image(path0, path1, quality=40, print_info=True)
>>> #convert_audio(path0, path1, bitrate='32k', print_info=True)
>>> #convert_video(path0, path1, resolution='640x480', bitrate='256k', print_info=True)
>>> 
>>> ## convert files with spcific ext inside a folder to another format
>>> folder_path = get_folderpath()
>>> audio_fp = get_filepaths_under(folder_path, filter=lambda p: p.endswith('.wav'))
>>> for input_path in audio_fp:
>>>     output_path = replace_ext(input_path, '.mp3')
>>>     convert_audio(input_path, output_path, bitrate='32k', print_info=True)
"""

from .pathkit import (
    get_filepath,
    get_filepaths,
    get_folderpath,
    get_filepaths_under,
    replace_ext,
)
from .convert import (
    convert_audio,
    convert_video,
    convert_image,
    get_file_size,
)