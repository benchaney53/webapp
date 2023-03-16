import PyPDF2

def extract_form_fields(input_pdf):
    pdf = PyPDF2.PdfReader(input_pdf)
    form_fields = {}

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]

        if '/Annots' not in page:
            continue

        annotations = page['/Annots']
        for annotation in annotations:
            annotation_object = pdf.get_object(annotation)
            if annotation_object['/Subtype'] == '/Widget' and '/T' in annotation_object:
                key = annotation_object['/T']
                form_fields[key] = ""

    return form_fields
