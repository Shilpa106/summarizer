from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .models import UploadFiles
from .serializers import UploadFilesSerializer
from upload.services import ocrContentReader



def home(request):
    return HttpResponse('Home')



class UploadFileView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = UploadFiles.objects.all().order_by('-created_at')
    serializer_class = UploadFilesSerializer
    lookup_field = 'id'

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
    
        for i in serializer.data:
            i.update({'ocr_content': ocrContentReader.ContentReader()})
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        serializer = UploadFilesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            f = request.FILES['upload_file']
            path = 'media/files/%s' % f.name

            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            destination.close()
            serializer.save() 

            serialize_data = serializer.data
            serialize_data.update({'ocr_content': ocrContentReader.ContentReader()})
            return Response(serialize_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# Views For Upload Handler
# from upload.services.uploadProgressCacheHandler import UploadProgressCacheHandler


# class UploadFileView(generics.CreateAPIView):
#     parser_classes = (MultiPartParser, FormParser)
#     queryset = UploadFiles.objects.all()
#     serializer_class = UploadFilesSerializer
#     lookup_field = 'id'

#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             request.upload_handlers.insert(0, UploadProgressCacheHandler(request))
#         serializer = UploadFilesSerializer(data=request.data)
        
        
#         if serializer.is_valid():
#             f = request.FILES['upload_file']
#             path = 'media/files/%s' % f.name

#             with open(path, 'wb+') as destination:
#                 for chunk in f.chunks():
#                     destination.write(chunk)
#             destination.close()
#             serializer.save() 

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# from django.core.cache import cache
# from django.http import HttpResponse, HttpResponseServerError 


# @api_view(['GET'])
# def upload_progress(request):
#     """
#     Return JSON object with information about the progress of an upload.
#     """
#     progress_id = ''
#     if 'X-Progress-ID' in request.GET:
#         progress_id = request.GET['X-Progress-ID']
#     elif 'X-Progress-ID' in request.META:
#         progress_id = request.META['X-Progress-ID']
#     if progress_id:
#         import json
#         cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
#         data = cache.get(cache_key)
#         return HttpResponse(json.dumps(data))
#     else:
#         return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')
