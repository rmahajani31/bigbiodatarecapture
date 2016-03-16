from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
import os.path
import re

def parseAllText(pdfpath, outputPath):
    resourceMgr = PDFResourceManager()
    laparams = LAParams()
    # textDevice = TextConverter(resourceMgr, pdfStr, codec=codec, laparams=laparams)
    device = PDFPageAggregator(resourceMgr, laparams=laparams)

    # textInterp = PDFPageInterpreter(resourceMgr, textDevice)
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
        extractCaptions(layout, captionList)

    captionFile = open(os.path.join(outputPath, paperName + ".txt"), 'w')
    for cap in captionList:
        captionFile.write("%s\n" % cap.encode('utf8'))
    captionFile.close()


def extractCaptions(layout, captionList):
    for ltObj in layout:
        if isinstance(ltObj, LTTextBox) or isinstance(ltObj, LTTextLine):
            text = ltObj.get_text()
            if (bool(re.match('figure', text, re.I)) or
                    bool(re.match('fig', text, re.I)) or
                    bool(re.match('diag', text, re.I)) or
                    bool(re.match('diagram', text, re.I)) or
                    bool(re.match('table', text, re.I))):
                captionList.append(text)
        elif isinstance(ltObj, LTFigure):
            extractCaptions(ltObj, captionList)

pdfPath = '../papers/AlteredAstrocyteMorphologyandVascularDevelopment.pdf'
output = '../captionOutputs/'
parseAllText(pdfPath, output)
