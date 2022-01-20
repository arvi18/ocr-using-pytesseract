from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name="home"),
    path('ocr/', views.OCRView, name="ocr"),
    path('ocr-pdf/', views.pdfOCRView, name="ocrpdf"),
]
