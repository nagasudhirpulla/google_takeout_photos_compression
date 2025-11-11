from moviepy.editor import VideoFileClip


def compressVideo(inputPath, outputPath, maxWidth=1280, audioQuality="high", mediaCreationTimeStr=""):
    # Load video clip
    videoClip = VideoFileClip(inputPath)
    try:
        # Set audio quality
        if audioQuality == "high":
            audioCodec = "aac"

        # get resize factor
        originalSize = videoClip.size
        maxWidthOriginal = max(originalSize[0], originalSize[1])
        resizeFactor = 1
        if maxWidthOriginal > maxWidth:
            resizeFactor = maxWidth/maxWidthOriginal

        if resizeFactor < 1:
            # resize video
            print(f"video resize factor = {resizeFactor}")
            videoClip = videoClip.resize(resizeFactor)

        # todo check if file size is ok as per new bit rate and cancel processing if video size in limits

        # Preserve the original video rotation
        rotation = videoClip.rotation
        # Rotate the video without cropping or stretching
        videoClip = videoClip.rotate(rotation)
        fps = 30
        bitsPerPixel = 0.05

        newBitrateKbps = originalSize[0]*originalSize[1] * \
            resizeFactor*resizeFactor*fps*bitsPerPixel*0.001

        ffmpegParams = None
        if not mediaCreationTimeStr == "":
            ffmpegParams = ['-metadata',
                            'creation_time=' + mediaCreationTimeStr]

        # Write the compressed video to the output path
        print(f"saving {outputPath}")
        videoClip.write_videofile(
            outputPath, codec="libx264", audio_codec=audioCodec,
            bitrate=f"{newBitrateKbps}k", fps=fps,
            ffmpeg_params=ffmpegParams)
        videoClip.close()
    except Exception as e:
        videoClip.close()
        print(f"Error compressing video {inputPath}: {str(e)}")
