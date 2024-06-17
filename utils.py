import os
from moviepy.editor import VideoFileClip, AudioFileClip
import logging

def download_and_combine_video(youtube, quality_options, selected_quality, download_audio, separate_audio, log_status, progressbar, success_callback, error_callback):
    try:
        stream = quality_options[selected_quality]
        if not download_audio:
            log_status("Downloading video without audio...")
            stream.download(filename="video_part.mp4")
            final_file = "video_part.mp4"
        elif stream.includes_audio_track:
            log_status("Downloading video with audio...")
            stream.download(filename="video.mp4")
            final_file = "video.mp4"
            log_status("Video downloaded successfully.")
        else:
            log_status("Downloading video without audio...")
            video_stream = youtube.streams.filter(res=stream.resolution, file_extension="mp4", only_video=True).first()
            log_status("Downloading video stream...")
            video_stream.download(filename="video_part.mp4")
            final_file = "video_part.mp4"
            if separate_audio:
                log_status("Downloading audio separately...")
                audio_stream = youtube.streams.filter(only_audio=True, file_extension="mp4").first()
                audio_stream.download(filename="audio_part.mp4")
                log_status("Audio downloaded successfully.")
            else:
                log_status("Downloading and combining audio...")
                audio_stream = youtube.streams.filter(only_audio=True, file_extension="mp4").first()
                audio_stream.download(filename="audio_part.mp4")
                log_status("Combining video and audio...")
                video_clip = VideoFileClip("video_part.mp4")
                audio_clip = AudioFileClip("audio_part.mp4")
                final_clip = video_clip.set_audio(audio_clip)
                final_file = "final_video.mp4"
                final_clip.write_videofile(final_file)
                video_clip.close()
                audio_clip.close()
                os.remove("audio_part.mp4")
                log_status("Video and audio combined successfully.")
        if os.path.exists("video_part.mp4"):
            os.remove("video_part.mp4")
        progressbar.stop()
        success_callback(final_file)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        progressbar.stop()
        error_callback(str(e))