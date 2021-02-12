from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import FeatureSerializer
from .models import ResultFeature
from DocumentUpload.models import UploadFiles
from DocumentFeature.models import ResultFeature, FeatureList

# from .services.ocrContentReader import ContentReader
from DocumentUpload.services.updateFeature import FetureThread

import threading
import os
from DocumentFeature import features
import json


"""
FeaturesList
    - Prepares the list of features yet to shift into database
"""
class FeaturesList(APIView):
    def get(self, request, format=None):
        feature = features.get_features()
        # print(feature)
        return Response({'features_list': feature}, status=status.HTTP_200_OK)


'''
getValue 
 - @params {class} - template 
'''
# def getValue(template : class, key : str, value) -> object: 
#     response = None
#     try:
#         response = template.objects.select_related(key).get(key=value)
#     except Exception as e:
#         print(e)

#     return response

"""
FeatureView
    - returns back the value based on the selected feature
"""
class FeatureView(APIView):
    
    def get(self, request, id, doc_id, format=None):
        try:
            # extracts the extension out of the file type 
            # getValue(ResultFeature, "docs_id", doc_id)
            docs_feature = ResultFeature.objects.select_related('docs_id').get(docs_id=doc_id)
        except Exception as e:
            for i in threading.enumerate():
                if i.name == str(doc_id):
                    print("Thread Name: ",i.name)
                    return Response({"Info": "We are processing your documnets, Please try after sometimes."})
            else:
                print("Else after for")
                pass
                # Celery task will perform here        
        try:
            feature = (FeatureList.objects.get(id=id))
            print("Feature-Title: ", feature)

            if docs_feature.docs_id.file_type == 'pdf':
                content = json.loads(docs_feature.body) #json.loads can be with for loop
                for i,j in content.items():
                    if i == str(feature.name):
                        return Response({str(i):j})
                else:
                    return Response({"Info":"We will add this feature soon"})
            else:
                return Response({'Info': 'Not a PDF document type', 'status': False})
        except Exception as e:
            return Response({"Info": "Feature Id didn't match something went wrong", 'status': False})
        
