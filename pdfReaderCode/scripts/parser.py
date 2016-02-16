from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import sys
from binascii import b2a_hex
import os.path

def parsePagesWithImages(pdfPath, outputImageFolder):
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
    count = 1

    for i, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)):
        print(count)
        generalInterp.process_page(page)
        textInterp.process_page(page)
        layout = device.get_result()
        num = parseLayout(layout, outputImageFolder, count)
        if num:
            num += 1
            count = num
        text = retstr.getvalue()
        txtFile = open(''+outputImageFolder+'/Paper1Page' + str(i) + '.txt', 'w')
        txtFile.write(text)
        txtFile.close()

    fp.close()
    device.close()
    textDevice.close()
    retstr.close()
    # print text

def parseLayout(layout, outputImageFolder, count):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTImage):
            print "IMAGE OBJECT"
            savedFile = saveImage(lt_obj, outputImageFolder, count)
            if savedFile:
                print "Image saved"
                return (count + 1)
            else:
                print >> sys.stderr, "error saving image", lt_obj.__repr__
                print "Error Saving Image"
        elif isinstance(lt_obj, LTFigure):
            parseLayout(lt_obj, outputImageFolder, count)

def saveImage(ltImage, outputImageFolder, count):
    """Try to save teh image data from this LTImage object. Returns the file
       if successful."""
    result = None
    if ltImage.stream:
        fileStream = ltImage.stream.get_rawdata()
        fileExt = determineImageType(fileStream[0:4])
        if fileExt:
            # fileName = 'Im' + str(count) + fileExt
            fileName = ltImage.name + fileExt
            if writeFile(outputImageFolder, fileName, fileStream, flags="wb"):
                result = fileName
    return result

def determineImageType(streamFirst4Bytes):
    """Find out the image file type based on the magic number comparison
       of the first 4 bytes"""

    fileType = None
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