from flask import *
from predict import fish
from datetime import datetime
from werkzeug.utils import secure_filename
app = Flask(__name__, template_folder='template')
# ใส่ path ของ model ของเรา
pred = fish("best.pt")

@app.route('/public/<path:path>')
def send_report(path):
    return send_from_directory('public', path)

@app.route('/')
def main():
 return render_template("index.html")

@app.route('/success', methods=['POST'])
def successPOST():
    if request.method == 'POST':
        files = request.files.getlist('files')
        date = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

        for f in files:
            filename = secure_filename(f.filename)
            f.save(f"public/{date}_{filename}")

            # Perform detection for each uploaded file
            detection = fish("best.pt")
            output_path = f"public/{date}_output_{filename}"
            detection(f"public/{date}_{filename}", output_path)

        return render_template("success.html", images=[f"public/{date}_output_{secure_filename(f.filename)}" for f in files])

    return redirect("/", code=302)
 
if __name__ == '__main__':
 app.run(debug=True, host='0.0.0.0',port=80)