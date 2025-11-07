from zipfile import ZipFile
from src.imageUtils import compressImage
from src.videoUtils import compressVideo
import glob
import pathlib
import os
import shutil

inpFolder = r'..\input'
outFolder = r"..\output"
maxImgWidthPx = 1280
qualityPerc = 100
audioQuality = "high"
tempFolderPath = "./temp"

numFiles = 0
numImgs = 0
numVids = 0
# get all zip file paths
for zipIter, zipFileName in enumerate(glob.glob(inpFolder+r"\\*.zip")):
    print(f"{zipIter} : processing zip {zipFileName}")
    with ZipFile(zipFileName, 'r') as zip:
        zipFilePaths = zip.namelist()
        for fPath in zipFilePaths:
            extractedFPath = ""
            if fPath.endswith(".jpg") or fPath.endswith(".mp4"):
                try:
                    shutil.rmtree(tempFolderPath)
                except Exception:
                    print(f"Unable to remove temp file {extractedFPath}")
                extractedFPath = zip.extract(fPath, tempFolderPath)
                numFiles += 1
                print(f"{numFiles} : processing {extractedFPath}")
                outFileName = pathlib.Path(extractedFPath).name
                outFilePath = os.path.join(outFolder, outFileName)
                
            if extractedFPath.endswith(".jpg"):
                numImgs += 1
                compressImage(extractedFPath, outFilePath, maxImgWidthPx, qualityPerc)
            elif extractedFPath.endswith(".mp4"):
                numVids += 1
                compressVideo(extractedFPath, outFilePath, maxImgWidthPx, audioQuality)

print(f"completed processing {numImgs} images, {numVids} videos, totalling {numFiles} files")