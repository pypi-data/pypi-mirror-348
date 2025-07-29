from pytubefix import YouTube
import subprocess
import os
import re

def download_highest_quality(url, output_path='./downloads'):
    """
    Downloads the absolute highest quality video and audio available

    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the final video
    """
    try:
        os.makedirs(output_path, exist_ok=True)
        yt = YouTube(url)

        # Clean title for filename
        title = yt.title
        safe_title = re.sub(r'[^\w\-_\. ]', '', title)
        base_filename = os.path.join(output_path, safe_title)

        print(f"\nDownloading: {title}")
        print(f"Duration: {yt.length // 60}:{yt.length % 60:02d}")
        print(f"Views: {yt.views:,}")
        print(f"Author: {yt.author}")

        # Get all progressive and adaptive streams
        print("\nAvailable video streams:")
        video_streams = yt.streams.filter(progressive=False, file_extension='mp4', type='video').order_by('resolution').desc()
        for i, stream in enumerate(video_streams):
            print(f"{i+1}. {stream.resolution} ({stream.fps}fps) | Codec: {stream.codecs[0] if stream.codecs else 'unknown'} | Bitrate: {stream.bitrate//1000 if stream.bitrate else '?'}kbps")

        # Select the highest quality video stream
        video_stream = video_streams.first()
        print(f"\nSelected video stream: {video_stream.resolution} ({video_stream.fps}fps)")

        # Get all audio streams
        print("\nAvailable audio streams:")
        audio_streams = yt.streams.filter(progressive=False, type='audio').order_by('abr').desc()
        for i, stream in enumerate(audio_streams):
            print(f"{i+1}. {stream.abr} | Codec: {stream.codecs[0] if stream.codecs else 'unknown'}")

        # Select the highest quality audio stream
        audio_stream = audio_streams.first()
        print(f"\nSelected audio stream: {audio_stream.abr}")

        # Download both streams
        print("\nDownloading streams...")
        video_file = video_stream.download(
            output_path=output_path,
            filename=f"{safe_title}_video.mp4"
        )
        audio_file = audio_stream.download(
            output_path=output_path,
            filename=f"{safe_title}_audio.{'mp4' if 'mp4' in audio_stream.mime_type else 'webm'}"
        )

        # Merge with FFmpeg
        output_file = f"{base_filename}_HQ.mp4"
        print("\nMerging with FFmpeg for maximum quality...")

        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',          # Copy video stream without re-encoding
            '-c:a', 'copy',          # Copy audio stream without re-encoding
            '-movflags', '+faststart',  # Enable streaming
            '-fflags', '+genpts',    # Generate missing PTS if needed
            '-shortest',             # Match to shortest stream
            '-y',                    # Overwrite without asking
            output_file
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"\n✅ Successfully created high quality file: {output_file}")

            # Verify output file
            verify_cmd = ['ffmpeg', '-i', output_file]
            result = subprocess.run(verify_cmd, capture_output=True, text=True)
            if 'Video: ' in result.stderr and 'Audio: ' in result.stderr:
                print("\nFile verification successful!")
                # Clean up temporary files
                os.remove(video_file)
                os.remove(audio_file)
                print("Temporary files removed.")
            else:
                print("\n⚠️ Warning: Output file verification failed")
                print("Keeping temporary files for manual inspection")

        except subprocess.CalledProcessError as e:
            print(f"\n❌ FFmpeg merge failed: {e}")
            print("Attempting alternative merge method...")

            # Try MKV container which is more forgiving
            output_file_mkv = f"{base_filename}_HQ.mkv"
            ffmpeg_cmd_mkv = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-c', 'copy',
                '-y',
                output_file_mkv
            ]

            try:
                subprocess.run(ffmpeg_cmd_mkv, check=True)
                print(f"\n✅ Successfully created high quality MKV file: {output_file_mkv}")
                os.remove(video_file)
                os.remove(audio_file)
                print("Temporary files removed.")
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Alternative merge also failed: {e}")
                print("Keeping separate video and audio files.")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

def check_ffmpeg():
    """Check if FFmpeg is installed and available in PATH"""
    try:
        subprocess.run(['ffmpeg', '-version'],
                      check=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("YouTube Highest Quality Downloader")
    print("---------------------------------")

    if not check_ffmpeg():
        print("\n❌ Error: FFmpeg is not installed or not in your PATH.")
        print("This script requires FFmpeg for merging high quality streams.")
        print("Please install FFmpeg:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/")
        exit(1)

    video_url = input("\nEnter YouTube video URL: ")
    download_highest_quality(video_url)

if __name__ == "__main__":
    main()