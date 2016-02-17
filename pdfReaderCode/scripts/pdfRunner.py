from parser import parseAllPagesWithImages

pdfpath = "../papers/1.pdf"
outputPath = "../paperAnalysis/1.txt"
imageFolder = "../paperAnalysis/"

parseAllPagesWithImages(pdfpath, imageFolder)
