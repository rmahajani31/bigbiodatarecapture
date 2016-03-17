from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
import os.path
import os
import re


BOX_INDEX = 0
LINE_INDEX = 1
IMAGE_INDEX = 2
ALL_CAPTIONS_INDEX = 0
ONLY_IMAGE_CAPTIONS_INDEX = 1

def parseAllText1(pdfpath, outputPath, captionAnalytics):
    resourceMgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resourceMgr, laparams=laparams)
    layoutInterp = PDFPageInterpreter(resourceMgr, device)

    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    match = re.search('/.+/(.+)\.pdf', pdfpath)
    paperName = match.group(1)

    fp = open(pdfpath, 'rb')
    captionList = []

    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)):
        layoutInterp.process_page(page)
        layout = device.get_result()
        extractCaptions(layout, captionList, captionAnalytics, outputPath, paperName)

def parseAllText2(pdfpath, outputPath, captionAnalytics):
    resourceMgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resourceMgr, laparams=laparams)
    layoutInterp = PDFPageInterpreter(resourceMgr, device)

    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    match = re.search('/.+/(.+)\.pdf', pdfpath)
    paperName = match.group(1)

    fp = open(pdfpath, 'rb')
    captionList = []

    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)):
        layoutInterp.process_page(page)
        layout = device.get_result()
        extractCaptionsUsingImages(layout, captionList, outputPath, paperName, captionAnalytics)


def extractCaptions(layout, captionList, analytics, outputPath, paperName):
    extractCaptionsHelper(layout, captionList, analytics)
    captionFile = open(os.path.join(outputPath, paperName + ".txt"), 'w')
    for cap in captionList:
        captionFile.write("%s\n" % cap.encode('utf8'))
    captionFile.close()


def extractCaptionsHelper(layout, captionList, analytics):
    for ltObj in layout:
        if isinstance(ltObj, LTTextBox) or isinstance(ltObj, LTTextLine):
            text = ltObj.get_text()
            if (bool(re.match('figure', text, re.I)) or
                    bool(re.match('fig', text, re.I)) or
                    bool(re.match('diag', text, re.I)) or
                    bool(re.match('diagram', text, re.I)) or
                    bool(re.match('table', text, re.I))):
                captionList.append(text)
                if isinstance(ltObj, LTTextBox):
                    analytics[BOX_INDEX] += 1
                elif isinstance(ltObj, LTTextLine):
                    analytics[LINE_INDEX] += 1
        elif isinstance(ltObj, LTFigure):
            extractCaptionsHelper(ltObj, captionList, analytics)

def extractCaptionsUsingImages(layout, captionList, outputPath, paperName, analytics):
    extractCaptionsUsingImagesHelper(layout, captionList, analytics)
    captionFile = open(os.path.join(outputPath, paperName + ".txt"), 'w')
    for i,cap in enumerate(captionList):
        captionFile.write("%s\n" % cap.encode('utf-8'))
        if i % 2 == 1:
            captionFile.write('\n')
    captionFile.close()

def extractCaptionsUsingImagesHelper(layout, captionList, analytics):
    imageFoundInThisLevel = False
    intermediateCaptionList = []
    for ltObj in layout:
        if isinstance(ltObj, LTTextBox):
            text = ltObj.get_text()
            if (bool(re.match('figure', text, re.I)) or
                    bool(re.match('fig', text, re.I)) or
                    bool(re.match('diag', text, re.I)) or
                    bool(re.match('diagram', text, re.I)) or
                    bool(re.match('table', text, re.I))):
                intermediateCaptionList.append(text)
                analytics[ALL_CAPTIONS_INDEX] += 1
        elif isinstance(ltObj, LTImage):
            imageFoundInThisLevel = True
            analytics[IMAGE_INDEX] += 1
            if len(intermediateCaptionList) == 0:
                captionList.append("IMAGE: " + str(ltObj.__repr__))
                captionList.append("CAPTION: ")
            for cap in intermediateCaptionList:
                captionList.append("IMAGE: " + str(ltObj.__repr__))
                captionList.append("CAPTION: " + cap)
                analytics[ONLY_IMAGE_CAPTIONS_INDEX] += 1
        elif isinstance(ltObj, LTFigure):
            extractCaptionsUsingImagesHelper(ltObj, captionList, analytics)


