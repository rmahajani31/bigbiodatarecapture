# from parser import parseAllPagesWithImages
from parser import parseAllText, parseTextAndImages
import os

allpapers = "../SERVERPapers/"
outputFolder = "../SERVERAnalysis/"

pdfpaths = os.listdir(os.path.join(os.getcwd(), allpapers))
for path in pdfpaths:
    newpath = ''.join(e for e in path if e.isalnum())
    newpath = newpath[0:-3] + ".pdf"
    path = os.path.join(allpapers, path)
    newpath = os.path.join(allpapers, newpath)

    os.rename(path, newpath)

    user = raw_input("about to parse: " + path)
    parseTextAndImages(newpath, outputFolder)

# parseTextAndImages(pdfpath, outputFolder)
