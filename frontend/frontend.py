from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(file.filename)
    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
