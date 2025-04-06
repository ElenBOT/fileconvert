## File Format Converter Tool
A collection of high-level helper functions that utilize ffmpeg and other modules to convert image, audio, and video files into different formats. Also, it support to adjust the quality of the files to reduce their size.

## Download
Directly download the code to use it. Donload as zip or using git:
```bash
git clone https://github.com/ElenBOT/fileconvert.git
```
> [!Note]
> user need to download `ffmpeg` first. Also modules that used in the code.

## Usage Example

```python
## convert files with spcific ext inside a folder to another format
from pathkit import *
from utility import *

folder_path = get_folderpath()
audio_fp = get_filepaths_under(folder_path, filter=lambda p: p.endswith('.wav'))
for input_path in audio_fp:
    output_path = replace_ext(input_path, '.mp3')
    convert_audio(input_path, output_path, bitrate='32k', print_info=True)
```

```python
## convert an (image, audio, video) to another format
from pathkit import *
from utility import *

path0 = get_filepath()
path1 = get_filepath(savefile=True)
convert_image(path0, path1, quality=40, print_info=True)
#convert_audio(path0, path1, bitrate='32k', print_info=True)
#convert_video(path0, path1, resolution='640x480', bitrate='256k', print_info=True)
```
