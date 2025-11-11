import os
from PIL import Image
import piexif
from fractions import Fraction
import datetime as dt


def copyImageMetadata(srcImgPath, destImgPath):
    # Open the source image
    srcImg = Image.open(srcImgPath)

    # Extract EXIF data from the source image
    if "exif" in srcImg.info:
        exifData = piexif.load(srcImg.info['exif'])

        # bug handling for 41729 exif tag (scenetype)
        if 41729 in exifData['Exif'] and isinstance(exifData['Exif'][41729], int):
            exifData['Exif'][41729] = str(
                exifData['Exif'][41729]).encode('utf-8')
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


def deg_to_dms(decimal_coordinate, cardinal_directions):
    """
    This function converts decimal coordinates into the DMS (degrees, minutes and seconds) format.
    It also determines the cardinal direction of the coordinates.

    :param decimal_coordinate: the decimal coordinates, such as 34.0522
    :param cardinal_directions: the locations of the decimal coordinate, such as ["S", "N"] or ["W", "E"]
    :return: degrees, minutes, seconds and compass_direction
    :rtype: int, int, float, string
    """
    # Source - https://stackoverflow.com/a/77056370
    if decimal_coordinate < 0:
        compass_direction = cardinal_directions[0]
    elif decimal_coordinate > 0:
        compass_direction = cardinal_directions[1]
    else:
        compass_direction = ""
    degrees = int(abs(decimal_coordinate))
    decimal_minutes = (abs(decimal_coordinate) - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = Fraction((decimal_minutes - minutes) * 60).limit_denominator(100)
    return degrees, minutes, seconds, compass_direction


def dms_to_exif_format(dms_degrees, dms_minutes, dms_seconds):
    """
    This function converts DMS (degrees, minutes and seconds) to values that can
    be used with the EXIF (Exchangeable Image File Format).

    :param dms_degrees: int value for degrees
    :param dms_minutes: int value for minutes
    :param dms_seconds: fractions.Fraction value for seconds
    :return: EXIF values for the provided DMS values
    :rtype: nested tuple
    """
    exif_format = (
        (dms_degrees, 1),
        (dms_minutes, 1),
        (int(dms_seconds.limit_denominator(100).numerator),
         int(dms_seconds.limit_denominator(100).denominator))
    )
    return exif_format


def get_gps_exif(latitude, longitude, altitude):
    """
    This function returns piexif GPS data from latitude and longitude
    This fumction calls the functions deg_to_dms and dms_to_exif_format.

    :param latitude: the north–south position coordinate
    :param longitude: the east–west position coordinate
    """
    # converts the latitude and longitude coordinates to DMS
    latitude_dms = deg_to_dms(latitude, ["S", "N"])
    longitude_dms = deg_to_dms(longitude, ["W", "E"])

    # convert the DMS values to EXIF values
    exif_latitude = dms_to_exif_format(
        latitude_dms[0], latitude_dms[1], latitude_dms[2])
    exif_longitude = dms_to_exif_format(
        longitude_dms[0], longitude_dms[1], longitude_dms[2])

    # https://exiftool.org/TagNames/GPS.html
    # Create the GPS EXIF data
    coordinates = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSLatitude: exif_latitude,
        piexif.GPSIFD.GPSLatitudeRef: latitude_dms[3],
        piexif.GPSIFD.GPSLongitude: exif_longitude,
        piexif.GPSIFD.GPSLongitudeRef: longitude_dms[3],
    }

    # return the EXIF data for the GPS information
    return coordinates


def getExifMetaData(jsonData: dict) -> dict:
    exif_dict = {}
    if "geoData" in jsonData:
        exifGpsData = get_gps_exif(
            jsonData.get("geoData", {}).get("latitude", 0),
            jsonData.get("geoData", {}).get("longitude", 0),
            jsonData.get("geoData", {}).get("altitude", 0)
        )
        exif_dict["GPS"] = exifGpsData

    photoCreationTimestampStr = jsonData.get(
        "photoTakenTime", {}).get("timestamp", "")
    if not photoCreationTimestampStr == "":
        photoCreationDt = dt.datetime.fromtimestamp(
            int(photoCreationTimestampStr), tz=dt.timezone.utc)
        exif_ifd = {
            piexif.ExifIFD.DateTimeOriginal: photoCreationDt.strftime("%Y:%m:%d %H:%M:%S"),
            piexif.ExifIFD.OffsetTimeOriginal: u"+:00:00",
        }
        exif_dict["Exif"] = exif_ifd
    return exif_dict


def getMediaCreationTimeStr(jsonData: dict) -> str:
    photoCreationTimestampStr = jsonData.get(
        "photoTakenTime", {}).get("timestamp", "")
    if not photoCreationTimestampStr == "":
        photoCreationDt = dt.datetime.fromtimestamp(
            int(photoCreationTimestampStr), tz=dt.timezone.utc)
        return photoCreationDt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return ""
