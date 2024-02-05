from flask import  Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'png', 'jpg', 'jpeg', 'gif'}

app=Flask(__name__)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and the file name is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFileName=f'static/{filename}'
            cv2.imwrite(newFileName, imgProcessed)
            return newFileName
        case "cwebp":
            newFileName=f'static/{filename.split(".")[0]}.webp'
            cv2.imwrite(newFileName, img)
            return newFileName
        case "cpng":
            newFileName=f'static/{filename.split(".")[0]}.png'
            cv2.imwrite(newFileName, img)
            return newFileName
        case "cjpg":
            newFileName=f'static/{filename.split(".")[0]}.jpg'
            cv2.imwrite(newFileName, img)
            return newFileName
           

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/edit',methods=["GET","POST"])
def  edit():
    if request.method=="POST":
        operation =  request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename, operation)
            flash(f"You image is processed and is availabel <a href='/{new}' target ='_blank'>here</a>")
            return render_template('index.html')
        
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug = True)
