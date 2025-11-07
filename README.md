* This script compresses the photos from zip files downloaded from google takeout and places the compressed photos and videos in a different folder location

## Algorithm
* Iterate through all the zip files in the input folder
* Iterate through each file inside the zip file (consider files that are in nested folders also)
* If the file is a jpg image, compress it if required and save it in the output folder
* If the file is a video, compress it if required and save it in the output folder
* Copy the exif metadata of the source file so that the metadata like GPS location, image taken date etc are intact in the compressed images and videos also  

### Image compression algorithm
* If width > height, max width should be 1280 px
* If height >  width, max height should be 1280 px
* Default JPEG image quality is 100, user can change this if required

### Video compression algorithm
* If width > height, max width should be 1280 px
* If height >  width, max height should be 1280 px
* Audio codec will be aac, default quality will be high
* Video codec will be H264

## References
* Video compression with moviepy- https://github.com/Sapansathawara/video_compressor_script_in_python/blob/main/video_compressor.py
* ffmeg, Handbrake, Shutter encoder tool for video compression
* photos compression like whatsapp with python pillow - https://nagasudhir.blogspot.com/2024/09/compress-photos-in-bulk-with-pillow.html