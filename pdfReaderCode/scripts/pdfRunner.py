from parser import parseAllPagesWithImages

pdfpath = "../papers/3.pdf"
outputPath = "../paperAnalysis/3.txt"
imageFolder = "../paperAnalysis/"

parseAllPagesWithImages(pdfpath, imageFolder)
