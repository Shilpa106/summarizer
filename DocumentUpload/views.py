from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.storage import default_storage

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .models import UploadFiles
from .serializers import UploadFilesSerializer
# from .services import ocrContentReader
from .services.updateFeature import FetureThread
from .services.driveupload import gServiceAccount, gDriveUpload
from .services.validatefiletype import validate_file_extension

import json
from datetime import datetime
from apiclient.http import MediaFileUpload, MediaIoBaseUpload
import io
import os
import threading


def home(request):
    design = '<h1 style="background-color:MediumSeaGreen;text-align:center;margin-top:250px;">Welcome to Summarizar!</h1>'
    return HttpResponse(design)



class UploadFileView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = UploadFiles.objects.all().order_by('-created_at')
    serializer_class = UploadFilesSerializer
    lookup_field = 'id'

    # def get(self, request, format=None):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True, context={'request': request})

        # for i in serializer.data:
        #     if i["upload_file"].endswith(".pdf"):
        #         path = i["upload_file"]
        #         new_path = path.split('/')  # spliting the file name from whole url
        #         abs_path = ''
        #         count = 3 # starting count 3 due to http[0], 127.....[1], path[2], <filename>.pdf[3] 
        #         for j in new_path[3:]:
        #             # appending / and scape / in the end for absolute path
        #             if count == (len(new_path)-1):
        #                 abs_path = abs_path + j
        #             else:
        #                 abs_path = abs_path + j + "/"
        #             count += 1
                
        #         i.update({'ocr_content': ocrContentReader.ContentReader(abs_path)})

        # return Response(serializer.data, status=status.HTTP_200_OK)



class UploadDocs(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    queryset = UploadFiles.objects.all().order_by('-created_at')
    serializer_class = UploadFilesSerializer
    lookup_field = 'id'


    def post(self, request, *args, **kwargs):
        try:
            serializer = UploadFilesSerializer(data=request.data, context={'request': request})
        except Exception as e:
            return Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)
        
        if validate_file_extension(serializer):
            if serializer.is_valid():
                f = request.FILES['upload_file']
                path = 'media/files/%s' % f.name

                get_link = gDriveUpload(f) # Function call to upload files on gDrive and get url

                arr = (f.name).split('.')
                metadata = {}
                metadata["name"] = f.name
                metadata["type"] = arr[-1]
                metadata["size"] = f.size
                metadata["created_at"] = datetime.now()
                jsondata = json.dumps(metadata, cls=DjangoJSONEncoder)

                serializer.validated_data["upload_file"] = get_link
                serializer.validated_data["file_type"] = metadata["type"]
                serializer.validated_data["file_size"] = f.size 
                serializer.validated_data["metadata"] = jsondata
                

                serializer.save()
                serialize_data = serializer.data
                docsid = serialize_data['id']
                if get_link:
                    with default_storage.open(f'{str(docsid)}{f.name}', 'wb+') as fs:
                        for chunk in f.chunks():
                            fs.write(chunk)
                        fs.close()
                    process = FetureThread(f'{f.name}', docsid)
                    process.name = docsid
                    process.daemon = True
                    process.start()
                    

                return Response(serialize_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Warning": "File type is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)



class UploadFileDetails(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = UploadFiles.objects.all()
    serializer_class = UploadFilesSerializer
    lookup_field = 'id'

    def get(self, request, id, *args, **kwargs):
        try:
            my_file = self.get_queryset().get(id=id)
            serializer = self.serializer_class(my_file, context={'request': request})
            serialized_data = serializer.data
            url = lambda uri : ('https:/' + uri.split('%3A')[1]) if '%3A' in uri else uri
            serialized_data['upload_file'] = url(serialized_data['upload_file'])
            return Response(serialized_data)
        except Exception as e:
            return Response({"Info": "Id not Found"})


class DocumentsByMe(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UploadFiles.objects.all()
    serializer_class = UploadFilesSerializer
    lookup_field = 'id'

    def get(self, request, format=None):
        docsList = self.get_queryset().filter(user_id=request.user)
        serializer = self.serializer_class(docsList, many=True, context={'request': request})
        for d in serializer.data:
            url = lambda uri : ('https:/' + uri.split('%3A')[1]) if '%3A' in uri else uri
            # print(url(d['upload_file']))
            d['upload_file'] = url(d['upload_file'])
        return Response(serializer.data, status=status.HTTP_200_OK)







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
