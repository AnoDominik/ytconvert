from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

# Ensure the downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'})

    # Generate unique filename
    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': output_path
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'success': True, 'download_url': f"/download/{video_id}"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/download/<video_id>')
def download_file(video_id):
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'success': False, 'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
