import json
from flask import Flask, request, render_template, jsonify, make_response, send_file, Response
from io import BytesIO
from pdf_form_extractor import extract_form_fields
import pdfrw

app = Flask(__name__)

from io import BytesIO

def fill_pdf(template_pdf, data):
    pdf = pdfrw.PdfReader(BytesIO(template_pdf.read()))
    for page in pdf.pages:
        annotations = page['/Annots'] if '/Annots' in page else []
        for annotation in annotations:
            if annotation['/Subtype'] == '/Widget' and '/T' in annotation:
                key = annotation['/T'][1:-1]  # Remove the parentheses around the field name
                if key in data:
                    annotation.update(pdfrw.PdfDict(V=f'{data[key]}'))
    output = BytesIO()
    pdfrw.PdfWriter().addpages(pdf.pages).write(output)
    output.seek(0)
    return output

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/pdf_extractor', methods=['GET', 'POST'])
def pdf_extractor():
    if request.method == 'POST':
        pdf_file = request.files['pdf-file']
        pdf_content = pdf_file.read()
        pdf_stream = BytesIO(pdf_content)
        extracted_data = extract_form_fields(pdf_stream)
        
        # Convert the extracted data to a JSON string
        json_data = json.dumps(extracted_data, indent=4)

        # Create a response with the JSON data and appropriate headers
        response = Response(json_data, content_type='application/json')
        response.headers.add('Content-Disposition', 'attachment', filename='extracted_data.json')
        return response

    return render_template('pdf_extractor.html')

@app.route('/edit_json', methods=['GET', 'POST'])
def edit_json():
    if request.method == 'POST':
        updated_data = request.get_json()
        with open('data.json', 'w') as f:
            json.dump(updated_data, f)
        return jsonify({'status': 'success'})
    return render_template('edit_json.html')

@app.route("/json_to_pdf", methods=["GET", "POST"])
def json_to_pdf():
    if request.method == "POST":
        input_json = request.files.get("input_json")
        template_pdf = request.files.get("template_pdf")
        if input_json is None or template_pdf is None:
            app.logger.error(f"input_json: {input_json}")
            app.logger.error(f"template_pdf: {template_pdf}")
            return make_response(jsonify({"error": "input_json and template_pdf are required"}), 400)

        # Rest of the code remains the same
        template_pdf_stream = BytesIO(template_pdf.read())
        input_json_stream = BytesIO(input_json.read())
        data = json.load(input_json_stream)
        filled_pdf = fill_pdf(template_pdf_stream, data)

        response = Response(filled_pdf.getvalue(), content_type='application/pdf')  # Call .getvalue() here
        response.headers.add('Content-Disposition', 'attachment', filename='filled_pdf.pdf')
        return response

    return render_template("upload_json.html")


if __name__ == "__main__":
    app.run(debug=True)
