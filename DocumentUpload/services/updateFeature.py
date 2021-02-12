from DocumentUpload.services.ocrContentReader import ContentReader
from DocumentFeature.models import ResultFeature
from DocumentUpload.models import UploadFiles

import threading
import time
import sys
import os
import json

class FetureThread(threading.Thread):
    def __init__(self, filepath, doc_id):
        self.filepath = filepath
        self.doc_id = doc_id
        # self.name = doc_id
        threading.Thread.__init__(self) # daemon=True

    def run(self):
        print("Waiting For 50 Seconds...")
        time.sleep(50)
        print(self.filepath)
        try:
            id = UploadFiles.objects.get(id=self.doc_id)
        except Exception as e:
            pass
        res = ContentReader(f'media/{str(self.doc_id)}{self.filepath}')
        body = json.dumps(res, indent=4)
        # print(body)
        print("Thread Name: ", self.name)
        if id:
            data = ResultFeature(docs_id=id, body=body)
            data.save()
        os.remove(f'media/{str(self.doc_id)}{self.filepath}')
        print("Hello, Data Saved")
        sys.exit()
    
