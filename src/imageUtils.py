import piexif
from PIL import Image


def compressImage(srcImgPath, destImgPath, maxWidth, quality=100, exifDict={}):
    # open source image
    image = Image.open(srcImgPath)

    # get the image dimensions
    width, height = image.size

    maxWidthOriginal = max(width, height)
    resizeFactor = 1
    if maxWidthOriginal > maxWidth:
        resizeFactor = maxWidth / maxWidthOriginal
    # Resize image if necessary
    if resizeFactor < 1:
        print(f"image resize factor = {resizeFactor}")
        image.thumbnail((width * resizeFactor, height * resizeFactor))

    # Save the new image
    outFname = destImgPath
    print(f"saving {outFname}")
    image.save(outFname, "JPEG", quality=quality, exif=piexif.dump(exifDict))

    # copy metadata from source image to destination image
    # copyImageMetadata(srcImgPath, destImgPath)
