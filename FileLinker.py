from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import send_from_directory
 
app = Flask(__name__)
         
app.secret_key = "caircocoders-ednalan"
 
#app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['UPLOAD_FOLDER'] = '/var/www/upload'
   
ALLOWED_EXTENSIONS = set(['mp4', 'webm', 'wmv', 'mov', 'avi', 'mpeg', 'mp3', 'pdf', 'm4a', 'jpg', 'jpeg', 'png', 'zip', 'rar', 'docx', 'doc', 'xls', 'xlsx'])
   
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def index(): 
    return render_template('index.html')
 
@app.route("/upload",methods=["POST","GET"])
def upload():
    file = request.files['uploadFile']
#    filesize = file.content_length			>>> FILE SIZE LIMITATION IS DONE In NGINX CONFIG FILE <<<
    filename = secure_filename(file.filename)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filenameimage = file.filename
        today = datetime.today() 
        msg  = "https://example.com/upload/" + filename #+ filesize 
###	Send each link to Bot
#        command = 'curl -k -s -S --max-time 15 -X GET "https://tapi.bale.ai/bot200957602:0866a9d3dc7bbf2923a54bc84138226c23752a37/sendMessage?chat_id=@technoline_events&text=' + msg + '" > /dev/null'
#        os.popen(command).close()
#        sizecommand = 'du -h -d0 /var/www/upload/ | awk {' + 'print $1' + '}'
#        size = os.popen(sizecommand).read()
#        total_upload_size = 'curl -k -s -S --max-time 15 -X GET "https://tapi.bale.ai/bot200957602:0866a9d3dc7bbf2923a54bc84138226c23752a37/sendMessage?chat_id=@technoline_events&text=' + size + '" > /dev/null'
#        os.popen(total_upload_size).close()
    else:
        msg  = 'Invalid file extension'
    return jsonify({'htmlresponse': render_template('response.html', msg=msg, filenameimage=filenameimage)})

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    #app.run(debug=True, host='127.0.0.1', port='5002')
    app.run(debug=False, port='5001')
