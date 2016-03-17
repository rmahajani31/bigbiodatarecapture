import captionCapture
import os
import os.path
import time

BOX_INDEX = 0
LINE_INDEX = 1
IMAGE_INDEX = 2
ALL_CAPTIONS_INDEX = 0
ONLY_IMAGE_CAPTIONS_INDEX = 1
captionAnalytics = [0,0,0]

def runAllPapers1():
    startTime = time.time()
    output = '../captionOutputs/'
    papersPath = '../SERVERPapers/'
    papersCaptionCapture = '../SERVERCaptionCaptureNoImages/'
    papersList = os.listdir(papersPath)
    for paper in papersList:
        captionCapture.parseAllText1(os.path.join(papersPath, paper), papersCaptionCapture, captionAnalytics)
    with open(os.path.join(papersCaptionCapture, 'summary.txt'), 'w') as f:
        f.write("Number of Captions in LTTextBoxes: %d\n" % captionAnalytics[BOX_INDEX])
        f.write("Number of Captions in LTTextLines: %d\n" % captionAnalytics[LINE_INDEX])

    endTime = time.time()
    print 'Execution time in seconds: ', (endTime - startTime)

def runAllPapers2():
    startTime = time.time()
    papersPath = "../SERVERPapers/"
    papersCaptionCapture = '../SERVERCaptionCaptureImages'
    papersList = os.listdir(papersPath)
    for paper in papersList:
        captionCapture.parseAllText2(os.path.join(papersPath, paper), papersCaptionCapture, captionAnalytics)
    with open(os.path.join(papersCaptionCapture, 'summary.txt'), 'w') as f:
        f.write("Number of Genearl Captions Found: %d\n" % captionAnalytics[ALL_CAPTIONS_INDEX])
        f.write("Number of Image Specific Captions Found: %d\n" % captionAnalytics[ONLY_IMAGE_CAPTIONS_INDEX])
        f.write("Number of Images Found: %d\n" % captionAnalytics[IMAGE_INDEX])

userin = raw_input("1 (no image intelligence), or 2 (with image intelligence)?")
if (userin == "1"):
    runAllPapers1()
else:
    runAllPapers2()