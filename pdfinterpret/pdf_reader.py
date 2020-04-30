from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.high_level import extract_pages

class PdfReader:

    def read_pdf(filename):
        with open(filename, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            return doc

    def get_pages(filename):
        return extract_pages(filename)

    