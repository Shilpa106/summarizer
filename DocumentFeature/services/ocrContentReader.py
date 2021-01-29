import PyPDF2
from PyPDF2 import PdfFileReader


def ContentReader(filepath, id):
    data = {}
    pdf = open(filepath, "rb")

    # Creating pdf reader object.
    pdf_reader = PyPDF2.PdfFileReader(pdf)

    if id == 2:
        num_pages = pdf_reader.getNumPages()
        data["No of Pages"] = num_pages
    elif id == 5:
        page = pdf_reader.getPage(0)
        content = page.extractText()
        data["Content"] = content
    else:
        data["Empty"] = "Empty"

    pdf.close()
    return data