from flask import Flask, render_template, request, send_from_directory
import pdf2docx
from werkzeug.utils import secure_filename
from util.todocx import convert_pdf2docx
# from werkzeug.datastructures import  FileStorage
import os

PORT = os.environ.get('PORT') or 3000
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads\\'
ALLOWED_EXTENSIONS = {'pdf'}


@app.route('/')
def uploader_file():
   return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      if f and allowed_file(f.filename):
         filename = secure_filename(f.filename)
         filename_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         filename_save_no_ext = filename.strip().split('.')[0]
         print(filename_save_no_ext)
         print('\033[31m################\033[m')
         filename_save_docx = filename_save_no_ext + '.docx'

         f.save(filename_save)

         convert_pdf2docx(filename_save, filename_save_docx)

         uploads = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
         # uploads = "C:\\Users\\ceifm\\Documents\\sites\\converter\\uploads\\" + filename_save_docx
         print(uploads, filename_save_docx)
         return send_from_directory(directory=uploads, filename=filename_save_no_ext+'.docx', as_attachment=True)
         # return "Ok"
      else:
         return "Sorry, just pdf files, please!"
   else:
      return "Sorry, just POST method allowed!"

app.run(host='0.0.0.0', port=PORT)
