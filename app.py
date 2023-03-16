from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get a list of all the image files in the directory
    image_files = [f for f in os.listdir('static/images') if f.endswith('.jpg') or f.endswith('.png')]

    # Render the template with the list of image files
    return render_template('index.html', image_files=image_files)

if __name__ == '__main__':
    app.run(debug=True)