
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os
from random import randint

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiftrail.settings")
application = get_wsgi_application()

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        file = open("my.file.pdf", "wb")
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}-{1}.pdf".format(params['request'].user.first_name, randint(1, 1000000))
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "store", file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]


Render.render('website/transaction-success.html', {})