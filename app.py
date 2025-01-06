from flask import Flask, request, render_template, send_file
import os
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        file_format = request.form.get("format")
        try:
            file_name = "video.mp4" if file_format == "mp4" else "audio.mp3"
            os.makedirs("downloads", exist_ok=True)

            result = subprocess.run(
                [
                    "yt-dlp",
                    "--cookies", "cookies.txt",
                    "-f", "bestaudio/best" if file_format == "mp3" else "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                    "-o", f"downloads/{file_name}",
                    url,
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                error_message = result.stderr
                return render_template("index.html", error=error_message)

            return send_file(f"downloads/{file_name}", as_attachment=True)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render platform esetén PORT változó
    app.run(host="0.0.0.0", port=port, debug=True)
