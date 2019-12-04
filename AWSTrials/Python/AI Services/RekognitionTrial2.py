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

def convertToBGR(a) :
    return a[:,:,::-1]

def show(imgFile, imgArray) :
    #img2 = imgArray[:,:,::-1]
    cv2.imshow(os.path.basename(imgFile), convertToBGR(imgArray))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def addRectanglesToImage(img, instancesInfo) :
    # Potential aLpha handling
    # https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
    # NB Using cv2 but array has RGB colouring
    bgrcolorRed = (255, 0, 0)
    bgrcolorGreen = (0, 255, 0)
    #bgrcolorYellow = (0, 255, 255)

    for info in instancesInfo :
        boxc = bgrcolorGreen if info['labelname'] == 'Person' else bgrcolorRed
        cv2.rectangle(img, (info['leftoffset'], info['topoffset'], info['width'], info['height']), color=boxc, thickness=2 )
        #cv2.rectangle(img, (info['leftoffset']-1, info['topoffset']-1, info['width']+2, info['height']+2), color=bgrcolorYellow, thickness=1 )

    return img

def writeImageFile(filename, imgArray) :
    cv2.imwrite(filename, convertToBGR(imgArray))
    print('Image file saved:', filename)

def addImageAt(top, left, amain, a) :
    # Check sizes and extend if necessary ?
    amain[top:top+a.shape[0],left:left+a.shape[1]] = a[:,:]
    return amain

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

    a = np.full((4000,imgShape[1] + 200,3), 255, dtype='uint8')

    #show(imgFile, a)

    leftIndent = 100
    verticalPoint = 100

    # Add the image to the array
    #a[100:100+imgShape[0],100:100+imgShape[1]] = imgArray[:,:]
    addImageAt(verticalPoint, leftIndent, a, imgArray)

    #show(imgFile, a)

    instancesInfo = rt1.extractInstancesInfo(imgArray, labelsResponse)

    # Add the image to the array
    #a[1200:1200+imgShape[0],100:100+imgShape[1]] = imgWithRectangles[:,:]
    #show(imgFile, a)

    #addCV2Text(a, summary)

    textArray = getPillowText(a, summary)
    textShape = textArray.shape
    verticalPoint = verticalPoint + imgArray.shape[0] + 100
    addImageAt(verticalPoint, leftIndent, a, textArray)

    #a[2400:2400+textShape[0],100:100+textShape[1]] = textArray[:,:]
    imgWithRectangles = addRectanglesToImage(imgArray.copy(), instancesInfo)
    verticalPoint = verticalPoint + textArray.shape[0] + 100
    addImageAt(verticalPoint, leftIndent, a, imgWithRectangles)

    # Add extracted images. Initially put each on a separate row, stop when out of room.
    # Should add some text to show label and confidence.
    verticalPoint = verticalPoint + imgWithRectangles.shape[0] + 100
    widthAvailable = a.shape[1] - leftIndent
    for info in instancesInfo :
        crop = info['crop']
        if verticalPoint + crop.shape[0] > a.shape[0] :
            print("Reached bottom of canvas - not displaying", crop.shape)
            # Or could copy to a bigger array ?
            newa = np.full((verticalPoint + crop.shape[0] + 100,a.shape[1],3), 255, dtype='uint8')
            addImageAt(0, 0, newa, a)
            a = newa
        #else :
        addImageAt(verticalPoint, leftIndent, a, crop)
        verticalPoint = verticalPoint + crop.shape[0] + 100
        print('Added ', crop.shape, verticalPoint)

    writeImageFile('output.jpg', a)

# #####################################################################################################

def addCV2Text(a, summary) :

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

    show('CV2Text', aText)

def getPillowText(ain, summary) :

    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype("cour.ttf", 20)
    pilImage = Image.fromarray(ain.astype('uint8'), 'RGB')
    draw = ImageDraw.Draw(pilImage, mode='RGBA')

    # Recreate the image as a Pillow image object from the numpy RGB image
    (textwidth, textheight) = draw.multiline_textsize(summary, font=font, spacing=0, stroke_width=0)
    print(textwidth, textheight)
    gap = 10

    a = np.full((textheight+2*gap,textwidth+2*gap,3), 255, dtype='uint8')

    # For Windows, available fonts are in C:/Windows/Fonts - Pillow seems to access this automatically.
    pilImage2 = Image.fromarray(a.astype('uint8'), 'RGB')
    draw2 = ImageDraw.Draw(pilImage2, mode='RGBA')

    top = gap
    left = gap
    xy_topleft = (left, top)
    draw2.multiline_text(xy_topleft, summary, font=font, fill=(0,0,0), spacing=0, stroke_width=0)

    npa = np.array(pilImage2)

    addRectangle = False
    if addRectangle :
        cv2.rectangle(npa, (0, 0, textwidth+2*gap, textheight+2*gap), color=(0,0,0), thickness=2 )

    show('PillowText', npa)

    return npa

if __name__ == '__main__' :    
    main(sys.argv)

