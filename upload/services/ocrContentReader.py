import PyPDF2
from PyPDF2 import PdfFileReader


def ContentReader(filepath):
    # // check for file existance
    # Creating a pdf file object.
    pdf = open(filepath, "rb")

    # Creating pdf reader object.
    pdf_reader = PyPDF2.PdfFileReader(pdf)

    # Checking total number of pages in a pdf file.
    print("Total number of Pages:", pdf_reader.numPages)

    # Creating a page object.
    page = pdf_reader.getPage(0)
    print(page)
    # Extract data from a specific page number.
    content = page.extractText()  # 200 
    # content = page.getContents()  # 200 
    print("Content ", content)
    # Closing the object.
    pdf.close()

    # // all your code here comes here..
    return content