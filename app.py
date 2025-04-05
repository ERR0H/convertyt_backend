from flask import Flask, request, send_file
import os
import yt_dlp

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    url = request.json.get('url')
    format_type = request.json.get('format')

    if not url or not format_type:
        return {"error": "URL and format are required"}, 400

    output_file = f"output.{format_type}"

    ydl_opts = {
        'format': 'bestaudio' if format_type == 'mp3' else 'bestvideo+bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio' if format_type == 'mp3' else 'FFmpegVideoConvertor',
            'preferredcodec': 'mp3' if format_type == 'mp3' else 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)