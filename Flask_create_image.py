from flask import Flask, render_template, request
from lib.DataModel import DataModel

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def uploader():
    """
    Basic file uploading using a form.
    Render template form if method is GET
    Create image and place in template if method is POST
    :return: rendered templates
    """
    print('I am in flas_create_image uploader')

    if request.method == 'GET':
        # default response when a form is called. Renders 'form/form_file_upload.html'
        return render_template('form/form_file_upload.html')

    elif request.method == 'POST':
        # response when the submit button is clicked in the 'form/form_file_upload.html'

        # get file from request object
        f = request.files['file']

        # Creates a DataModel object and calls the bar.plot() method passing the file from the file upload
        x = DataModel()
        results = x.create_fig(f)

        # resulting barplot is passed to the the HTML_visualization_template.html rendered page
        return render_template('HTML_CSS_templates/HTML_visualization_template.html', results=results, title="Outputpage")
