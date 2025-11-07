from PIL import Image
from src.metadataUtils import copyImageMetadata

def compressImage(srcImgPath, destImgPath, maxWidth, quality=100):
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
    image.save(outFname, 'JPEG', quality=quality)

    # copy metadata from source image to destination image
    copyImageMetadata(srcImgPath, destImgPath)
