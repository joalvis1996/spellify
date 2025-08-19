# app.py
from flask import Flask, request, render_template, send_from_directory, url_for
import os, uuid
from capture import capture_fullpage_gif

app = Flask(__name__)

RESULT_DIR = os.path.join('static', 'results')
os.makedirs(RESULT_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # 매번 다른 이름으로 저장(캐시/중복 방지)
        output_file = f"{uuid.uuid4().hex}.gif"
        output_path = os.path.join(RESULT_DIR, output_file)

        capture_fullpage_gif(url, output_path, duration=3, capture_fps=10)

        # 미리보기 + 자동다운로드 트리거
        return render_template('index.html', result_gif=output_file)

    return render_template('index.html')

@app.route('/results/<filename>')
def result_file(filename):
    # 미리보기용(브라우저에 표시)
    return send_from_directory(RESULT_DIR, filename, mimetype='image/gif')

@app.route('/download/<filename>')
def download_file(filename):
    # 강제 다운로드용
    return send_from_directory(
        RESULT_DIR,
        filename,
        as_attachment=True,
        mimetype='image/gif',
        download_name=filename,
    )
