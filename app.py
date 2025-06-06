from flask import Flask, request, jsonify
import threading
import requests
import os

app = Flask(__name__)

def download_and_process(video_url):
    try:
        response = requests.get(video_url)
        if response.status_code != 200:
            print("Failed to download video")
            return

        with open("video.mp4", "wb") as f:
            f.write(response.content)

        print("✅ Video saved successfully!")

        # Devamına buradan transcribe ve edit adımları eklenebilir

    except Exception as e:
        print("🔥 Background error:", str(e))

@app.route("/")
def home():
    return "🟢 Replit RenderClip is running!"

@app.route("/upload-url", methods=["POST"])
def upload_url():
    try:
        data = request.get_json(force=True)
        video_url = data.get("url")
        if not video_url:
            return jsonify({"error": "Missing 'url' field"}), 400

        thread = threading.Thread(target=download_and_process, args=(video_url,))
        thread.start()

        return jsonify({"status": "Processing started"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
