from flask import Flask, request, jsonify, send_file
import threading
import requests
import os
from utils import transcribe_audio, find_best_segment, edit_video

app = Flask(__name__)

def process_video(video_url):
    try:
        response = requests.get(video_url)
        if response.status_code != 200:
            print("❌ Video indirilemedi.")
            return

        with open("video.mp4", "wb") as f:
            f.write(response.content)
        print("✅ Video başarıyla indirildi.")

        transcript = transcribe_audio("video.mp4")
        print("📝 Transkript çıkarıldı.")

        start, duration, highlight_text = find_best_segment(transcript)
        print(f"🎯 En iyi segment: Başlangıç={start}, Süre={duration}")

        edit_video("video.mp4", start, duration, transcript, highlight_text)
        print("🎬 Video düzenlendi ve final.mp4 olarak kaydedildi.")

    except Exception as e:
        print("🔥 Hata:", str(e))

@app.route("/")
def home():
    return "🚀 RenderClip Shorts Editör çalışıyor!", 200

@app.route("/upload-url", methods=["POST"])
def upload_url():
    try:
        data = request.get_json(force=True)
        print("📩 Gelen veri:", data)

        video_url = data.get("url")
        if not video_url:
            return jsonify({"error": "Missing 'url' field"}), 400

        threading.Thread(target=process_video, args=(video_url,)).start()
        return jsonify({"status": "Video processing started"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["GET"])
def download():
    return send_file("final.mp4", as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
