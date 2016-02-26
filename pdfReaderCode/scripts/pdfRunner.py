# from parser import parseAllPagesWithImages
from parser import parseAllText, parseTextAndImages
import os

allpapers = "../papers/"
outputFolder = "../paperAnalysis/"

pdfpaths = os.listdir(os.path.join(os.getcwd(), allpapers))
for path in pdfpaths:
    path = os.path.join(allpapers, path)
    user = raw_input("about to parse: " + path)
    parseTextAndImages(path, outputFolder)

# parseTextAndImages(pdfpath, outputFolder)
