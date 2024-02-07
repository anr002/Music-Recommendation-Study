from pytube import YouTube
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import os


def download_video(url, target_folder):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    if not stream:
        print("No audio stream found")
        return None

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    mp4_file_path = stream.download(output_path=target_folder)
    print(f"Downloaded mp4 file path: {mp4_file_path}")

    wav_file_path = os.path.splitext(mp4_file_path)[0] + '.wav'
    audio_clip = AudioFileClip(mp4_file_path)
    audio_clip.write_audiofile(wav_file_path)
    audio_clip.close()
    print(f"Converted to wav file path: {wav_file_path}")

    os.remove(mp4_file_path)
    print(f"Deleted original mp4 file: {mp4_file_path}")

    return wav_file_path

def convert_to_wav(filename, target_folder, title):
    new_filename = os.path.join(target_folder, title + '.wav')
    audio_clip = AudioSegment.from_wav(filename)
    snippet = audio_clip
    snippet.export(new_filename, format="wav")
    print(f"Exported new wav file: {new_filename}")
    return new_filename