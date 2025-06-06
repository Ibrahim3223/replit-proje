import whisper
import moviepy.editor as mp
from moviepy.video.fx.all import crop
import os

model = whisper.load_model("base")

def transcribe_audio(video_path):
    result = model.transcribe(video_path)
    return result  # includes ['segments']

def find_best_segment(transcript):
    segments = transcript.get("segments", [])
    if not segments:
        return 0, 15, ""

    best = max(segments, key=lambda x: x['end'] - x['start'])
    start = int(best['start'])
    end = int(best['end'])
    duration = min(end - start, 15)

    text = best['text']
    return start, duration, text

def edit_video(video_path, start, duration, transcript, highlight_text):
    # Load video
    clip = mp.VideoFileClip(video_path).subclip(start, start + duration)

    # Crop to vertical (centered)
    width, height = clip.size
    if width > height:
        delta = (width - height) // 2
        clip = crop(clip, x1=delta, x2=delta)

    # Add subtitle
    txt = mp.TextClip(highlight_text, fontsize=60, color='white', bg_color='black', size=clip.size, method='caption')
    txt = txt.set_duration(clip.duration).set_position(("center", "bottom"))

    # Hook: "You won't believe this moment..."
    hook = mp.TextClip("You won't believe this moment...", fontsize=70, color='red', bg_color='black', size=clip.size)
    hook = hook.set_duration(2).set_position("center")

    final = mp.concatenate_videoclips([hook, mp.CompositeVideoClip([clip, txt])])
    final = final.set_audio(clip.audio)
    final.write_videofile("final.mp4", codec="libx264", audio_codec="aac")
