import os
from PIL import Image
import piexif

def copyImageMetadata(srcImgPath, destImgPath):
    # Open the source image
    srcImg = Image.open(srcImgPath)

    # Extract EXIF data from the source image
    if "exif" in srcImg.info:
        exifData = piexif.load(srcImg.info['exif'])

        # bug handling for 41729 exif tag (scenetype)
        if 41729 in exifData['Exif'] and isinstance(exifData['Exif'][41729], int):
            exifData['Exif'][41729] = str(exifData['Exif'][41729]).encode('utf-8')
    else:
        exifData = {}
    
    # Open the destination image
    destImg = Image.open(destImgPath)

    # Save the destination image with the source's EXIF data
    destImg.save(destImgPath, exif=piexif.dump(exifData))

    # Copy file attributes for last accessed time and modified time
    srcImgStats = os.stat(srcImgPath)

    # set file ownership information (applicable only in unix systems)
    # os.chown(destImgPath, srcImgStats.st_uid, srcImgStats.st_gid)

    # set modified time and last accessed time
    os.utime(destImgPath, (srcImgStats.st_atime, srcImgStats.st_mtime))