from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from subprocess import Popen
import re
from os import path
import os

def parseAllText(pdfPath, outputFolder):
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
    txtFile = open('' + outputFolder + '/Paper' + paperName + 'AllText.txt', 'w')
    txtFile.write(text)
    txtFile.close()
    fp.close()
    textDevice.close()
    retstr.close()
    return paperName
    # print text

def parseTextAndImages(pdfpath, outputFolder):
    paperName = parseAllText(pdfpath, outputFolder)
    outputImageFolder = path.join(outputFolder, paperName + "Images")
    print outputImageFolder
    if not path.isdir(outputImageFolder):
        os.makedirs(outputImageFolder)
    imageCommand = "pdfimages  " + pdfpath + " " + path.join(outputImageFolder, paperName)
    print "imageCommand: " + imageCommand
    raw_input("good?")
    Popen(imageCommand, shell=True)
