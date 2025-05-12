from flask import Flask, request, render_template, send_from_directory
import os
from capture import capture_fullpage_gif

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        output_file = 'output.gif'
        output_path = os.path.join('static/results', output_file)

        os.makedirs('static/results', exist_ok=True)

        capture_fullpage_gif(
            url,
            output_path,
            duration=3,
            capture_fps=10
        )

        return render_template('index.html', result_gif=output_file)

    return render_template('index.html')

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory('static/results', filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
