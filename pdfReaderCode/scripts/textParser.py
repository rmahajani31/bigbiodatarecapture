from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from subprocess import call
import re

def parseAllText(pdfPath, outputImageFolder):
    resourceMgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    textDevice = TextConverter(resourceMgr, retstr, codec=codec, laparams=laparams)
    textInterp = PDFPageInterpreter(resourceMgr, textDevice)
    fp = open(pdfPath, 'rb')
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    match = re.search('/.+/(.+)\.pdf', pdfPath)
    paperName = match.group(1)

    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)):
        textInterp.process_page(page)
        text = retstr.getvalue()
        txtFile = open('' + outputImageFolder + '/Paper' + paperName + 'Page' + str(i+1) + '.txt', 'w')
        txtFile.write(text)
        txtFile.close()

    fp.close()
    textDevice.close()
    retstr.close()
    imageCommand = "pdfimages -j " + pdfPath + " " + outputImageFolder
    call(imageCommand, shell=True)
    # print text