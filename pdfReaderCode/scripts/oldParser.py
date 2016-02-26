from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import sys
from binascii import b2a_hex
import os.path
import random
import pdb
import re
import os.path

def parseAllPagesWithImages(pdfPath, outputImageFolder):
    resourceMgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    textDevice = TextConverter(resourceMgr, retstr, codec=codec, laparams=laparams)
    device = PDFPageAggregator(resourceMgr, laparams=laparams)
    generalInterp = PDFPageInterpreter(resourceMgr, device)
    textInterp = PDFPageInterpreter(resourceMgr, textDevice)
    fp = open(pdfPath, 'rb')
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    imageCount = 1
    match = re.search('/.+/(.+)\.pdf', pdfPath)
    paperName = match.group(1)

    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)):
        generalInterp.process_page(page)
        textInterp.process_page(page)
        layout = device.get_result()
        # pdb.set_trace() # Start debugging
        imageCount = parseLayout(layout, outputImageFolder, imageCount)
        text = retstr.getvalue()
        txtFile = open('' + outputImageFolder + '/Paper' + paperName + 'Page' + str(i+1) + '.txt', 'w')
        txtFile.write(text)
        txtFile.close()

    fp.close()
    device.close()
    textDevice.close()
    retstr.close()
    # print text

def parseLayout(layout, outputImageFolder, numImages):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTImage):
            savedFile = saveImage(lt_obj, outputImageFolder, numImages)
            if savedFile:
                numImages += 1
                # print "Image saved"
                # print "Image number is ", numImages
            else:
                print >> sys.stderr, "error saving image", lt_obj.__repr__
                filters = lt_obj.stream.get_filters()
                print filters
                # randomInt = str(int(random.random() * 1000))
                # fp = open(os.path.join(outputImageFolder, (randomInt + '.dat')), 'w')
                # fp.write(lt_obj.stream.get_rawdata())
                # fp.close()
        elif isinstance(lt_obj, LTFigure):
            # print "Recursive call"
            parseLayout(lt_obj, outputImageFolder, numImages)
    return numImages

def saveImage(ltImage, outputImageFolder, numImages):
    """Try to save the image data from this LTImage object. Returns the file
       if successful."""
    result = None
    if ltImage.stream:
        fileStream = ltImage.stream.get_rawdata()
        fileExt = determineImageType(fileStream[0:4])
        if fileExt:
            randomInt = int(random.random() * 1000)
            fileName = ltImage.name + str(randomInt) + fileExt
            # fileName = ltImage.name + str(numImages) + fileExt
            if writeFile(outputImageFolder, fileName, fileStream, flags="wb"):
                result = fileName
    return result

def determineImageType(streamFirst4Bytes):
    """Find out the image file type based on the magic number comparison
       of the first 4 bytes"""

    fileType = '.ppm'
    bytesAsHex = b2a_hex(streamFirst4Bytes)
    if bytesAsHex.startswith("ffd8"):
        fileType = '.jpeg'
    elif bytesAsHex == '89504e47':
        fileType = '.png'
    elif bytesAsHex == '47494638':
        fileType = '.gif'
    elif bytesAsHex.startswith('424d'):
        fileType = '.bmp'
    return fileType

def writeFile(outputImageFolder, fileName, fileData, flags='w'):
    """Write the file data to the folder and filename combination
       (flags: 'w' for write text, 'wb' for write binary, use 'a'
        instea)d of 'w' for append)"""
    result = False
    if os.path.isdir(outputImageFolder):
        try:
            fileObj = open(os.path.join(outputImageFolder, fileName), flags)
            fileObj.write(fileData)
            fileObj.close()
            result = True
        except IOError:
            pass
    return result

def writePdfToTxtFile(text, path):
    output = open(path, 'w')
    output.write(text)
    output.close()
