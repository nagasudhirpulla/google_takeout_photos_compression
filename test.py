# from zipfile import ZipFile
# fileName = r"..\input\takeout-20251107T044436Z-1-001.zip"
# with ZipFile(fileName, 'r') as zip:
#     zipFilePaths = zip.namelist()
#     imageFilePaths = [x for x in zipFilePaths if x.endswith(".jpg")]
#     print(imageFilePaths)
#     # read image using 
#     # img = Image.open(zip.open(imageFilePaths[0]))
#     vidFilePaths = [x for x in zipFilePaths if x.endswith(".mp4")]
#     print(vidFilePaths)

from zipfile import ZipFile
import ffmpeg
fileName = r"..\input\takeout-20251107T044436Z-1-001.zip"
with ZipFile(fileName, 'r') as zip:
    zipFilePaths = zip.namelist()
    vidFilePaths = [x for x in zipFilePaths if x.endswith(".mp4")]
    # videoClip = VideoFileClip(zip.open(vidFilePaths[0]))
    vid = ffmpeg.probe(zip.open(vidFilePaths[0]))
    print(vid['streams'])