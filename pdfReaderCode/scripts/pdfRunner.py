# from parser import parseAllPagesWithImages
from textParser import parseAllText

pdfpath = "../papers/3.pdf"
outputPath = "../paperAnalysis/3.txt"
imageFolder = "../paperAnalysis/"

# parseAllPagesWithImages(pdfpath, imageFolder)
parseAllText(pdfpath, imageFolder)
