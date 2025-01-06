from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')  # A HTML fájl neve

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        video_url = data.get('url')
        if not video_url:
            return jsonify({'error': 'No URL provided'}), 400

        output_format = data.get('format', 'mp4')  # Alapértelmezett formátum MP4
        options = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        # Formátum beállítása
        if output_format == 'mp3':
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif output_format == 'mp4':
            options['format'] = 'bestvideo+bestaudio/best'

        # Fájl letöltése
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
            if output_format == 'mp3':
                file_path = file_path.replace('.webm', '.mp3').replace('.mp4', '.mp3')

        return jsonify({'message': 'Download complete', 'file_path': file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
