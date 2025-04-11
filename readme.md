## File Format Converter Tool
A collection of high-level helper functions that utilize ffmpeg, exiftool and other modules to convert image, audio, and video files into different formats and reduce the quality as well as file size.

## Download
Directly download the code to use it. Donload as zip or using git:
```bash
git clone https://github.com/ElenBOT/fileconvert.git
```
> [!Note]
> User need to download `ffmpeg` and python modules that used in the code first.
> While `exiftool` is optioanl, it deal with information in picture like GPS location and camera parameters.

## Usage Example

```python
## convert an (image, audio, video) to another format
from pathkit import *
from convert import *

input_path = get_filepath()
output_path = get_filepath(savefile=True)
convert_image(input_path, output_path, quality=40, print_info=True)
#convert_audio(input_path, output_path, bitrate='32k', print_info=True)
#convert_video(input_path, output_path, resolution='640x480', bitrate='256k', print_info=True)
```

```python
## convert files with spcific ext inside a folder to another format
from pathkit import *
from convert import *

folder_path = get_folderpath()
audio_filepaths = get_filepaths_under(folder_path, filter=lambda p: p.endswith('.wav'))
for input_path in audio_filepaths:
    output_path = replace_ext(input_path, '.mp3')
    convert_audio(input_path, output_path, bitrate='32k', print_info=True)
```

