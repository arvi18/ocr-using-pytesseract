from .models import Upload
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from ocr_using_pytesseract.settings import MEDIA_ROOT
from .models import Upload

# Create your views here.


def HomeView(req):
    return render(req, "base.html")


def OCRView(req):
    if(req.POST):
        from django.core.files.storage import default_storage
        #  Reading file from storage
        # file = default_storage.open(file_name)
        # file_url = default_storage.url(file_name)

        file = req.FILES["file-upload"]

        if file.name.endswith(".pdf"):
            isPDF = True

            file_instance = Upload.objects.create(upload_file=file)
            file_url = MEDIA_ROOT+"\\"+str(file_instance)

            from .ocr import pdfToImg
            text = pdfToImg(file_url, str(file_instance))
        else:
            isPDF = False
    else:
        isPDF = False
        text = None
    return render(req, "ocr.html", {'isPDF': isPDF, 'text': text})