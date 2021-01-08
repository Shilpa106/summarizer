from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.home),
    path('my/documents/', views.DocumentsByMe.as_view(), name='my-documents'),
    path('upload-list/', views.UploadFileView.as_view(), name='upload-list'),
    path('upload/new/', views.UploadDocs.as_view(), name='upload-new'),
    path('upload/<int:id>', views.UploadFileDetails.as_view(), name='upload-details'),
]
