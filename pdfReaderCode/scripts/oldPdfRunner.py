from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
import re
from binascii import b2a_hex
import random
import os.path
import sys

def printAllElements(pdfpath, output):
    resourceMgr = PDFResourceManager()
    codec = "utf-8"
    laparams = LAParams()
    device = PDFPageAggregator(resourceMgr, laparams=laparams)
    generalPageInterp = PDFPageInterpreter(resourceMgr, device)

    fp = open(pdfpath, 'rb')
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    imageCount = 1

    match = re.search('/.+/(.+)\.pdf', pdfpath)
    paperName = match.group(1)

    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)):
        generalPageInterp.process_page(page)
        layout = device.get_result()
        parseLayout(layout, output, i)


def parseLayout(layout, outputImageFolder, pageNum):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTImage):
            raw_input("Image Detected. Proceed?")
            savedFile = saveImage(lt_obj, outputImageFolder, pageNum)
            if savedFile:
                print "Image saved"
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
            parseLayout(lt_obj, outputImageFolder, pageNum)

def saveImage(ltImage, outputImageFolder, pageNum):
    """Try to save the image data from this LTImage object. Returns the file
       if successful."""
    result = None
    if ltImage.stream:
        # print "ltImage type: " + str(type(ltImage.stream))
        fileStream = ltImage.stream.get_rawdata()
        # print "raw data type: " + str(type(fileStream))
        fileExt = determineImageType(fileStream[0:4])
        if fileExt:
            randomInt = int(random.random() * 1000)
            # fileName = ltImage.name + str(randomInt) + fileExt
            fileName = "Page" + str(pageNum) + ltImage.name + fileExt
            if writeFile(outputImageFolder, fileName, fileStream, flags="wb"):
                result = fileName
    return result

def determineImageType(streamFirst4Bytes):
    """Find out the image file type based on the magic number comparison
       of the first 4 bytes"""

    fileType = None
    bytesAsHex = b2a_hex(streamFirst4Bytes)
    print bytesAsHex
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
            firstfour = fileData[0:4]
            rest = fileData[4:]
            fileObj = open(os.path.join(outputImageFolder, fileName), 'wb')
            if b2a_hex(firstfour).startswith("789c"):
                print "Weird Byte If Entered!"
                fileObj.write('\xFF\xD8\xFF\xE0')
                fileObj.write(rest)
            else:
                print "JPEG If Entered!"
                fileObj.write(fileData)
            fileObj.close()
            result = True
        except IOError:
            pass
    return result


pdfpath = "../papers/3.pdf"
output = "./myScriptImageOutput"
printAllElements(pdfpath, output)