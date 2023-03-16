from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        # Do something with the JSON data
        return jsonify({'message': 'Data received successfully!'})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
