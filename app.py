import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'secret'

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            photo = form.photo.data
            filename = photo.filename
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully!'
    return render_template('upload.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
