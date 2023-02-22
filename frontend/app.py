from flask import Flask, render_template, request
from costapp_web import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])

def upload_file():
    file = request.files['file']
    output, row, col, cost = find_row_and_column(1150, 2.5, file)
    print(f"The cost for a {row} quality rated home with {col} sq.ft. is ${cost:,.2f}")
    #file.save(file.filename)

    return render_template("cost_template.html", output=output, row=row, col=col, cost=cost)

if __name__ == '__main__':
    app.run(debug=True)
