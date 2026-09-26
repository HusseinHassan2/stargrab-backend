import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # يسمح لتطبيقك بالاتصال بالسيرفر بدون مشاكل أمان

@app.route('/')
def home():
    return jsonify({"status": "Server is running successfully!"})

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    # خيارات استخراج الرابط المباشر بجميع الجودات
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'downloadUrl': info.get('url'),
                'platform': info.get('extractor_key', 'Unknown')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
