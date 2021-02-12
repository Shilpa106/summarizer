import PyPDF2
from PyPDF2 import PdfFileReader

import io
import os
import requests
from urllib.request import urlopen, Request


"""
ContentReader
    - Based on the library, it performs the file based operation which ever applicable 
    - later on would get replaced by Factory Pattern later on for providing support for pdf, images , and other doc types
"""
def ContentReader(filepath):
    data = {}
    
    pdf = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)

    no_of_pages = pdf_reader.getNumPages()
    page = pdf_reader.getPage(0)
    content = page.extractText()
    data['Total no of Pages'] = no_of_pages
    data['Content'] = content
    
    # if feature_id == 2:
    #     content = pdf_reader.getNumPages()
    # elif feature_id == 5:
    #     page = pdf_reader.getPage(0)
    #     content = page.extractText()
    #     # data["Content"] = content
    # elif feature_id == 8:
    #     content = "value for another one.. "
    # else:
    #     feature_title = "Empty"
    #     content = "Empty"
    #     # data["Empty"] = "Empty"

    # data[feature_title] = content

    pdf.close()
    return data