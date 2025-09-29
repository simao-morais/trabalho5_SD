import os
from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video_file' not in request.files:
        return 'Nenhum arquivo enviado.'

    video_file = request.files['video_file']
    if video_file.filename == '':
        return 'Nenhum arquivo selecionado.'

    if video_file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(video_path)

        audio_filename = os.path.splitext(video_file.filename)[0] + '.mp3'
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)

        try:
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(audio_path)
            clip.close()
            os.remove(video_path)
            return send_file(audio_path, as_attachment=True)
        except Exception as e:
            return f'Erro durante a conversão: {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)