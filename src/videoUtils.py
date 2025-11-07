from moviepy.editor import VideoFileClip

def compressVideo(inputPath, outputPath, resolution=(1920, 1080), audioQuality="high"):
    # todo max width 1280
    try:
        # Load video clip
        videoClip = VideoFileClip(inputPath)

        # Set audio quality
        if audioQuality == "high":
            audioCodec = "aac"

        # Preserve the original video rotation
        rotation = videoClip.rotation

        # Rotate the video without cropping or stretching
        rotatedClip = videoClip.rotate(rotation)

        # Set resolution after rotation
        rotatedClip = rotatedClip.resize(resolution)

        # Write the compressed video to the output path
        rotatedClip.write_videofile(outputPath, codec="libx264", audio_codec=audioCodec)

        print(f"saving {outputPath}")
    except Exception as e:
        print(f"Error compressing {inputPath}: {str(e)}")
