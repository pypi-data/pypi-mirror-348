# agh-vqis
A Python package computing a set of image quality indicators (IQIs) for a given input video.

Following IQIs are included in the package:

- A set of 15 Video Quality Indicators (VQIs) developed by the team from AGH. See the following website for more information: https://qoe.agh.edu.pl/indicators/.
- Our Python reimplementation of the Colourfulness IQI. See [this](http://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf) paper for more information regarding this IQI.
- Blur Amount IQI. See [package's Python Package Index web page](https://pypi.org/project/cpbd/) for more information.
- UGC IQI (User-generated content).

**Authors**: Jakub Nawała <[jakub.nawala@agh.edu.pl](mailto:jnawala@agh.edu.pl)>, Filip Korus <[fkorus@student.agh.edu.pl](mailto:fkorus@student.agh.edu.pl)>

## Requirements
- ffmpeg - version >= 4.4.2
- Python - version >= 3.9

## Installation
```shell
pip install agh_vqis
```

### Usage
1. Single multimedia file:
    ```python
    from agh_vqis import process_single_mm_file, VQIs
    from pathlib import Path
    
    if __name__ == '__main__':
        process_single_mm_file(Path('/path/to/single/video.mp4'))
    ```


2. Folder with multimedia files:
    ```python
    from agh_vqis import process_folder_w_mm_files, VQIs
    from pathlib import Path
    
    if __name__ == '__main__':
        process_folder_w_mm_files(Path('/path/to/multimedia/folder/'))
   ```


3. Options parameter - in either `process_single_mm_file` and `process_folder_w_mm_files` function options could be provided as an optional argument. It is being passed to function as a dictionary like below.
    ```python
     process_single_mm_file(Path('/path/to/single/video.mp4'), options={
          VQIs.contrast: False,  # disable contrast indicator
          VQIs.colourfulness: False,  # disable colourfulness indicator
     })
    ```
   

4. How to disable/enable indicators to count? Every indicator is **enabled by default except `blur_amount`** due to long computing time. To disable one of following indicators `(blockiness, SA, letterbox, pillarbox, blockloss, blur, TA, blackout, freezing, exposure, contrast, interlace, noise, slice, flickering, colourfulness, ugc)` pass 
   ```python
   VQIs.indicator_name: False
   ```
   to options dictionary. Whereas to **enable** `blur_amount` indicator pass `True` value.


5. agh-vqis package could be used from command line interface as well. For example:
   ```shell
   python3 -m agh_vqis /path/to/single/movie.mp4 # will run VQIS for single file
   ```
   or
   ```shell
   python3 -m agh_vqis /path/to/multimedia/folder/ # will run VQIS for folder
   ```
   Whereas this command will display help:
   ```shell
   $ python3 -m agh_vqis -h
   ```
6. Supported multimedia files: `mp4`, `y4m`, `mov`, `mkv`, `avi`, `ts`, `webm`, `jpg`, `jpeg`, `png`, `gif`, `bmp`.


7. First row of the output CSV file contains header with image quality indicators (IQIs) names, whereas each row below the header represents single video frame from the input video file. Each column provides a numerical result as returned by a given IQI when applied to the respective frame.


8. Cast chosen indicators for different resolutions (**experimental**). For example: to cast Blur to 1440p and Blockiness to 2160p you should pass two additional lines in `options` dictionary like below.
   ```python
       from agh_vqis import process_single_mm_file, CastVQI, DestResolution
       from pathlib import Path
       
       if __name__ == '__main__':
           process_single_mm_file(Path('/path/to/single/video.mp4'), options={
              CastVQI.blur: DestResolution.p1440,
              CastVQI.blockiness: DestResolution.p2160
           })
      ```

   ### Available casts (with percentage of correctness)
   #### Blockiness:
   | source resolution | destination resolution | correctness |
   |-------------------|------------------------|-------------|
   | 1080p             | 1440p                  | 99.80%      |
   | 1080p             | 2160p                  | 99.72%      |
   | 1440p             | 2160p                  | 99.68%      |
   | 2160p             | 1440p                  | 99.81%      |

   #### Blur:
   | source resolution | destination resolution | correctness |
   |-------------------|------------------------|-------------|
   | 240p              | 360p                   | 93.91%      |
   | 240p              | 480p                   | 87.78%      |
   | 360p              | 240p                   | 94.28%      |
   | 360p              | 480p                   | 98.08%      |
   | 360p              | 720p                   | 92.51%      |
   | 480p              | 240p                   | 87.68%      |
   | 480p              | 360p                   | 98.05%      |
   | 480p              | 720p                   | 97.35%      |
   | 720p              | 360p                   | 92.69%      |
   | 720p              | 480p                   | 97.31%      |
   | 720p              | 1080p                  | 80.95%      |
   | 1080p             | 1440p                  | 99.12%      |
   | 1080p             | 2160p                  | 93.41%      |
   | 1440p             | 1080p                  | 99.07%      |
   | 1440p             | 2160p                  | 96.24%      |
   | 2160p             | 1080p                  | 93.59%      |
   | 2160p             | 1440p                  | 96.39%      |
   
   #### Exposure(bri):
   | source resolution | destination resolution | correctness |
   |-------------------|------------------------|-------------|
   | 240p              | 360p                   | 97.75%      |
   | 240p              | 480p                   | 94.89%      |
   | 240p              | 720p                   | 89.71%      |
   | 360p              | 240p                   | 97.77%      |
   | 360p              | 480p                   | 98.68%      |
   | 360p              | 720p                   | 94.83%      |
   | 360p              | 1080p                  | 80.37%      |
   | 480p              | 240p                   | 94.82%      |
   | 480p              | 360p                   | 98.68%      |
   | 480p              | 720p                   | 97.80%      |
   | 480p              | 1080p                  | 82.90%      |
   | 480p              | 1440p                  | 80.40%      |
   | 720p              | 240p                   | 89.32%      |
   | 720p              | 360p                   | 94.87%      |
   | 720p              | 480p                   | 97.85%      |
   | 720p              | 1080p                  | 86.99%      |
   | 720p              | 1440p                  | 84.66%      |
   | 720p              | 2160p                  | 82.34%      |
   | 1080p             | 360p                   | 80.71%      |
   | 1080p             | 480p                   | 83.41%      |
   | 1080p             | 720p                   | 86.88%      |
   | 1080p             | 1440p                  | 98.78%      |
   | 1080p             | 2160p                  | 96.91%      |
   | 1440p             | 480p                   | 80.90%      |
   | 1440p             | 720p                   | 84.85%      |
   | 1440p             | 1080p                  | 98.83%      |
   | 1440p             | 2160p                  | 99.05%      |
   | 2160p             | 720p                   | 82.89%      |
   | 2160p             | 1080p                  | 96.93%      |
   | 2160p             | 1440p                  | 98.98%      |
   
   #### Contrast:
   | source resolution | destination resolution | correctness |
   |-------------------|------------------------|-------------|
   | 240p              | 360p                   | 99.83%      |
   | 240p              | 480p                   | 99.69%      |
   | 240p              | 720p                   | 99.55%      |
   | 240p              | 1080p                  | 87.94%      |
   | 240p              | 1440p                  | 87.94%      |
   | 240p              | 2160p                  | 87.91%      |
   | 360p              | 240p                   | 99.85%      |
   | 360p              | 480p                   | 99.97%      |
   | 360p              | 720p                   | 99.93%      |
   | 360p              | 1080p                  | 88.36%      |
   | 360p              | 1440p                  | 88.34%      |
   | 360p              | 2160p                  | 88.36%      |
   | 480p              | 240p                   | 99.73%      |
   | 480p              | 360p                   | 99.97%      |
   | 480p              | 720p                   | 99.98%      |
   | 480p              | 1080p                  | 88.61%      |
   | 480p              | 1440p                  | 88.67%      |
   | 480p              | 2160p                  | 88.67%      |
   | 720p              | 240p                   | 99.61%      |
   | 720p              | 360p                   | 99.93%      |
   | 720p              | 480p                   | 99.98%      |
   | 720p              | 1080p                  | 88.45%      |
   | 720p              | 1440p                  | 88.46%      |
   | 720p              | 2160p                  | 88.46%      |
   | 1080p             | 240p                   | 87.12%      |
   | 1080p             | 360p                   | 87.71%      |
   | 1080p             | 480p                   | 87.82%      |
   | 1080p             | 720p                   | 87.91%      |
   | 1080p             | 1440p                  | 99.99%      |
   | 1080p             | 2160p                  | 99.99%      |
   | 1440p             | 240p                   | 87.13%      |
   | 1440p             | 360p                   | 87.72%      |
   | 1440p             | 480p                   | 87.85%      |
   | 1440p             | 720p                   | 87.92%      |
   | 1440p             | 1080p                  | 99.99%      |
   | 1440p             | 2160p                  | 100.0%      |
   | 2160p             | 240p                   | 87.11%      |
   | 2160p             | 360p                   | 87.72%      |
   | 2160p             | 480p                   | 87.85%      |
   | 2160p             | 720p                   | 87.91%      |
   | 2160p             | 1080p                  | 99.99%      |
   | 2160p             | 1440p                  | 100.0%      |
   
   #### Interlace:
   | source resolution | destination resolution | correctness |
   |-------------------|------------------------|-------------|
   | 240p              | 360p                   | 86.93%      |
   | 360p              | 240p                   | 87.19%      |
   | 360p              | 480p                   | 88.32%      |
   | 480p              | 360p                   | 87.22%      |
   | 480p              | 720p                   | 90.80%      |
   | 720p              | 480p                   | 91.21%      |
   | 720p              | 1080p                  | 82.65%      |
   | 1080p             | 1440p                  | 81.35%      |
   
   #### Noise:
   | source resolution | destination resolution | correctness |
   |-------------------|------------------------|-------------|
   | 240p              | 360p                   | 88.85%      |
   | 360p              | 240p                   | 88.08%      |
   | 360p              | 480p                   | 86.33%      |
   | 480p              | 360p                   | 85.94%      |
   | 480p              | 720p                   | 88.71%      |
   | 720p              | 480p                   | 88.12%      |
   | 1080p             | 1440p                  | 94.84%      |
   | 1080p             | 2160p                  | 80.34%      |
   | 1440p             | 1080p                  | 92.28%      |
   | 1440p             | 2160p                  | 87.24%      |
   | 2160p             | 1440p                  | 88.54%      |


### License
The `agh-vqis` Python package is provided via the [Evaluation License Agreement](https://app.qoe.agh.edu.pl/public/agh-vqis/license.txt).
