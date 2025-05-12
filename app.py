from flask import Flask, request, render_template, send_from_directory
import os
from capture import capture_fullpage_webp

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        output_file = 'output.webp'
        output_path = os.path.join('static/results', output_file)

        # WebP 움짤 캡처 실행 (품질 최적화 적용)
        capture_fullpage_webp(
            url,
            output_path,
            duration=5,
            capture_fps=15,    # 캡처는 15fps
            playback_fps=5,    # 재생은 5fps (느리게 보이게)
            quality=85,
            method=6
        )

        return render_template('index.html', result_webp=output_file)
    return render_template('index.html')

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory('static/results', filename)

if __name__ == '__main__':
    app.run(debug=True)

