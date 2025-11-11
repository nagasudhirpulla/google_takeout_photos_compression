from PIL import Image
import piexif

def compressImage(srcImgPath, destImgPath, maxWidth, quality=100, exifDict={}):
    # open source image
    image = Image.open(srcImgPath)

    # get the image dimensions
    width, height = image.size

    # Resize image if necessary
    if width > maxWidth:
        newHeight = height*(maxWidth/width)
        image.thumbnail((maxWidth, newHeight))

    # Save the new image
    outFname = destImgPath
    print(f"saving {outFname}")
    image.save(outFname, 'JPEG', quality=quality, exif=piexif.dump(exifDict))

    # copy metadata from source image to destination image
    # copyImageMetadata(srcImgPath, destImgPath)
