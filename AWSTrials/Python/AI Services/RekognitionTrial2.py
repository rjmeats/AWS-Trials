import sys
import os

import numpy as np
from cv2 import cv2

import RekognitionTrial1 as rt1

def getImageArray(imgFile) :

    # Read in the image, with MatPlotLib providing a 3-D numpy array
    # Dimensions of the numpy array are:
    # - y axis, moving down from the top of the image to the bottom
    # - x axis, moving from the left side of the image to right
    # - colour, as three separate values, for R,G,B
    import matplotlib.image as mpimg 
    imageArray = mpimg.imread(imgFile) 
    return imageArray

def getSummaryText(imgFile, labelsResponse) :

    from io import StringIO

    temp_out = StringIO()
    current_out = sys.stdout
    sys.stdout = temp_out
    rt1.dumpLabelInfo(imgFile, labelsResponse)
    sys.stdout = current_out
    return temp_out.getvalue()

def show(imgFile, imgArray) :
    cv2.imshow(os.path.basename(imgFile), imgArray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def addRectanglesToImage(img, instancesInfo) :
    # Potential aLpha handling
    # https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
    bgrcolorRed = (0, 0, 255)
    bgrcolorGreen = (0, 255, 0)
    #bgrcolorYellow = (0, 255, 255)

    for info in instancesInfo :
        boxc = bgrcolorRed if info['labelname'] == 'Person' else bgrcolorGreen
        cv2.rectangle(img, (info['leftoffset'], info['topoffset'], info['width'], info['height']), color=boxc, thickness=2 )
        #cv2.rectangle(img, (info['leftoffset']-1, info['topoffset']-1, info['width']+2, info['height']+2), color=bgrcolorYellow, thickness=1 )

    return img

def writeImageFile(filename, imgArray) :
    cv2.imwrite(filename, imgArray)
    print('Image file saved:', filename)

def main(argv) :

    if len(argv) > 1 and argv[1] != '-' :
        imgFile = argv[1]
    else :
        imgFile = 'AI Services/woodbridge.jpg'
        print('No image file argument provided, using default : ', imgFile)

    if len(argv) > 2 :
        tool = argv[2]
    else :
        tool = 'MatPlotLib'
        print('No tool argument provided, using default : ', tool)

    # Process the image file
    labelsResponse = rt1.detectLabelsFromLocalFile(imgFile)
    summary = getSummaryText(imgFile, labelsResponse)
    print()
    print(summary)
    print()
    rt1.dumpLabelInfo(imgFile, labelsResponse)

    imgArray = getImageArray(imgFile)
    imgShape = imgArray.shape

    print()
    print('Image array type is {0}, shape is {1}'.format(type(imgArray), imgArray.shape))

    a = np.full((3000,3000,3), 255, dtype='uint8')

    show(imgFile, a)

    # Add the image to the array
    a[100:100+imgShape[0],100:100+imgShape[1]] = imgArray[:,:]

    show(imgFile, a)

    instancesInfo = rt1.extractInstancesInfo(imgArray, labelsResponse)
    imgWithRectangles = addRectanglesToImage(imgArray.copy(), instancesInfo)

    # Add the image to the array
    a[1200:1200+imgShape[0],100:100+imgShape[1]] = imgWithRectangles[:,:]

    show(imgFile, a)

    addText(a, summary)

    writeImageFile('output.jpg', a)

# #####################################################################################################

def addText(a, summary) :

    # Trial writing out text using with CV2 font - not very nice looking. And no fixed-width font.
    # Pillow may work better.
    font = cv2.FONT_HERSHEY_SIMPLEX
    lineCount = 0
    maxHeight = 0
    maxWidth = 0
    for line in enumerate(summary.split('\n')):
        lineCount += 1
        s = line[1]
        (width, height), baseline = cv2.getTextSize(s, font, fontScale=1, thickness=2)
        print(height, width, baseline, s)
        maxHeight = max(maxHeight, height)
        maxWidth = max(maxWidth, width)

    aText = np.full(((maxHeight+20) * lineCount, maxWidth+20,3), 255, dtype='uint8')

    print('Lines = ', lineCount)
    print('Maxh, Maxw =', maxHeight, maxWidth)
    print('Shape is', aText.shape)

    for line in enumerate(summary.split('\n')):
        i = line[0]
        text_offset_x = 10
        text_offset_y = i * (maxHeight+20)
        cv2.putText(aText, line[1], (text_offset_x, text_offset_y), font, fontScale=1, thickness=1, color=(0, 0, 0))

    show('Text', aText)

if __name__ == '__main__' :    
    main(sys.argv)

