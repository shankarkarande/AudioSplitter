from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def split_audio(file_path):
    song = AudioSegment.from_file('uploads/audio.wav')
    segment_duration = 60 * 1000  # 1 minute in milliseconds
    num_segments = len(song) // segment_duration

    segments = []
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = (i + 1) * segment_duration
        segment = song[start_time:end_time]
        segment.export(os.path.join(app.config['UPLOAD_FOLDER'], f"segment_{i + 1}.wav"), format="wav")
        segments.append(f"segment_{i + 1}.wav")

    return segments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        segments = split_audio(file_path)
        print("File saved to:", file_path)
        return render_template('index.html', segments=segments)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
