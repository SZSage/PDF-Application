from PyPDF2 import PdfFileMerger, PdfFileReader
import os


def merge_pdf():
    path = "/users/Sage/Documents/Coding/PDFMerge"
    os.chdir(path)  # change directory
    merger = PdfFileMerger()
    for pdf in os.listdir(path):  # for each PDF
        with open(pdf, "rb"):
            if pdf.endswith("pdf"):  # if files end with pdf, merge to new pdf file
                merger.append(pdf)  # adds to file
    merger.write("Merged PDF.pdf")
    print("PDF Merged")


merge_pdf()
