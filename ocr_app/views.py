from .models import Upload
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from ocr_using_pytesseract.settings import MEDIA_ROOT
from .models import Upload

# Create your views here.

def HomeView(req):
    return render(req, "home.html")

def OCRView(req):
    if(req.POST):
        easyOCR=False
        addBorder=False
        removeBorder=False
        deskew=False
        for key in req.POST.keys():
            if key=='easyOCR':
                easyOCR=True
            if key=='addBorder':
                addBorder=True
            if key=='removeBorder':
                removeBorder=True
            if key=='deskew':
                deskew=True

        file = req.FILES["file-upload"]

        file_instance = Upload.objects.create(upload_file=file)
        file_url = MEDIA_ROOT+"\\"+str(file_instance)

        from .ocr import imgToText
        text = imgToText(file_url, str(file_instance), easyOCR, addBorder, removeBorder, deskew)
    else:
        text = None
        return render(req, "ocr.html")
    return render(req, "ocr.html", {'text': text})

def pdfOCRView(req):
    if(req.POST):
        easyOCR=False
        addBorder=False
        removeBorder=False
        deskew=False
        for key in req.POST.keys():
            if key=='easyOCR':
                easyOCR=True
            if key=='addBorder':
                addBorder=True
            if key=='removeBorder':
                removeBorder=True
            if key=='deskew':
                deskew=True
        # from django.core.files.storage import default_storage
        #  Reading file from storage
        # file = default_storage.open(file_name)
        # file_url = default_storage.url(file_name)

        file = req.FILES["file-upload"]

        if file.name.endswith(".pdf"):
            isPDF = True

            file_instance = Upload.objects.create(upload_file=file)
            file_url = MEDIA_ROOT+"\\"+str(file_instance)

            from .ocr import pdfToImg
            text = pdfToImg(file_url, str(file_instance), easyOCR, addBorder, removeBorder, deskew)
        else:
            isPDF = False
            return render(req, "ocr_pdf.html")
    else:
        isPDF = False
        text = None
        return render(req, "ocr_pdf.html")
    return render(req, "ocr_pdf.html", {'text': text})