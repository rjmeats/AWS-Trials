# Program to display an image and the items identified within it by Amazon Rekognition, using
# a single combined output file. The output file is itself an image showing:
# - the original image
# - a summary of the Rekognition results
# - the original image with rectangles applied to it to highlight 'instances' (people, cars, ...)
#   found by Rekognition
# - and then the instance rectangles are displayed one-by-one, with a confidence score
#
# See the RekognitionTrial1 module for detailed Rekognition interaction.
#
# Image manipulation is performed using a combination of tools(!):
# - Matplotlib, to read the original image into an RGB numpy array, and saving the final
#   image to an output file 
# - Pillow, to convert text strings to image form
# - CV2 for drawing rectangles and displaying intermediate images
# - and some direct numpy array manipulation (to copy images onto other images)
#
# Images within the program are held as 3-D numpy arrays.
# The dimensions of the numpy array are:
# - y axis, moving down from the top of the image to the bottom
# - x axis, moving from the left side of the image to right
# - colour, as three separate values, for R,G,B (defaulting to white as a background)
#
# When using Pillow, these arrays have to be converted to a Pillow image object.
# When using CV2, allowance needs to be made for CV2 treating the colour values as being BGR instead of RGB.

# #####################################################################################################

import sys
import os

import numpy as np

import RekognitionTrial1 as rt1

# #####################################################################################################

def readImageArrayFromFile(imgFile) :
    """ Read the source image file into a 3-D numpy array [y,x,RGB] """

    import matplotlib.image as mpimg 
    imgArray = mpimg.imread(imgFile)

    # Matplotlib produces the numpy array in the correct format. No need to modify it.
    return imgArray

def writeImageArrayToFile(filename, imgArray) :
    """ Write an image array out to a jpg file """

    import matplotlib.image as mpimg 
    mpimg.imsave(filename, imgArray, format='jpg')
    print('Image file saved: {0}'.format(filename))

# Alternative write-image-to-file function using CV2 - works, but not used
def writeImageArrayToFileUsingCV2(filename, imgArray) :

    from cv2 import cv2
    cv2.imwrite(filename, convertToBGR(imgArray))
    print('Image file saved: {0}'.format(filename))


# Diagnostics function, to see intermediate images during development. The Window remains open until you
# press a key.
def showImage(title, imgArray) :
    """ Display an image in a CV2 window """

    # For CV2 we need to reverse the colour ordering of the array to BGR
    from cv2 import cv2
    cv2.imshow(title, convertToBGR(imgArray.copy()))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# #####################################################################################################

def getSummaryText(imgFile, labelsResponse) :
    """ Return multiline summary text about the image and the items in Rekognition's label response """

    # The rt1 module has a function which produces the text we want, but prints it to stdout instead 
    # of producing a string. So redirect stdout to a StringIO object while we call the rt1 function,
    # and then create the string object from the StringIO object.
    from io import StringIO

    tempStdOut = StringIO()
    savedStdOut = sys.stdout
    sys.stdout = tempStdOut
    rt1.dumpLabelInfo(imgFile, labelsResponse)
    sys.stdout = savedStdOut

    return tempStdOut.getvalue()

# #####################################################################################################

# Functions doing direct image numpy array manipulation without using other libraries.

def newImageArray(y, x) :
    """ Create a new image array of dimensions [y,x,RGB], set to all white """
    return np.full((y,x,3), 255, dtype='uint8')

def extendImage(imgArray, newy, newx) :
    """ Return a new (larger) image array of dimensions [newy, newx, RGB] containing the existing image at [0,0]. """

    # Could check that the new image will be at least as large, otherwise the slice copy will fail ?
    imgArrayNew = newImageArray(newy, newx)
    imgArrayNew[0:imgArray.shape[0], 0:imgArray.shape[1]] = imgArray[:,:]
    return imgArrayNew

def addImageAt(imgArray, imgArrayToAdd, ytop, xleft) :
    """ Returns an image formed by adding an image at the specified position to an existing image, 
    extending it if necessary """

    # print('Adding image of shape {0} to image of shape {1} at point ({2},{3})'.format(
    #         imgArrayToAdd.shape, imgArray.shape, ytop, xleft))

    ybottom = ytop + imgArrayToAdd.shape[0]
    xright = xleft + imgArrayToAdd.shape[1]

    # Check if placing the additional image at the specified position will go beyond the current 
    # image's array boundary. If so, extend it, before copying in the additional image.    
    if ybottom > imgArray.shape[0] :
        imgArray = extendImage(imgArray, ybottom, imgArray.shape[1])
        # print('Image array extended down - new shape is {0}'.format(imgArray.shape))

    if xright > imgArray.shape[1] :
        imgArray = extendImage(imgArray, imgArray.shape[0], xright)
        # print('Image array extended right - new shape is {0}'.format(imgArray.shape))

    imgArray[ytop:ybottom, xleft:xright] = imgArrayToAdd[:,:]
    return imgArray

def convertToBGR(imgArray) :
    """ Converts a 3-D [y,x,RGB] numpy array to [y,x,BGR] format, (for use with CV2) """
    return imgArray[:,:,::-1]

# #####################################################################################################

def addRectangleToImage(imgArray, instanceInfo, RGBColourMap) :
    """ Use 'instance info' obtained from Rekognition to draw a rectangle in the specified colour around 
        the labelled instance located in the main image. """

    # Use CV2 for this. NB We specify colours as RGB, as that is what we're using for the array. But if we
    # ever used CV2's colours, they would be BGR and so need reversing to match the rest of the array.
    from cv2 import cv2

    # Potential CV2 aLpha handling if ever required
    # https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c

    RGBColourWhite = (255, 255, 255)

    for info in instanceInfo :        
        RGBColour = RGBColourMap.get(info['labelname'], RGBColourWhite)
        cv2.rectangle(imgArray, (info['leftoffset'], info['topoffset'], info['width'], info['height']), color=RGBColour, thickness=2 )

    return imgArray

# #####################################################################################################

def getTextAsImageArray(text, fontFile="cour.ttf", fontPointSize=25, ymargin=10, xmargin=10) :
    """ Return a 3-D [y,x,RGB] numpy image array which displays the specified text, black text on white.

        - this uses Pillow
        - on Windows, the available font file names are in C:/Windows/Fonts
    """

    # Do this in stages:
    # - get Pillow to tell us how big the image will need to be
    # - create an image array large enough
    # - get Pillow to write the text to the new image array.

    # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype(fontFile, fontPointSize)

    # We need a Pillow 'Draw' object to perform text operations with. To determine the size, 
    # we still need to give it an 'image' to work with - use a dummy one.
    dummyImageArray = newImageArray(100,100)
    pilImage = Image.fromarray(dummyImageArray.astype('uint8'), 'RGB')
    draw = ImageDraw.Draw(pilImage, mode='RGBA')

    spacing = 2         # Number of pixels between lines
    strokeWidth = 0     # Thinnest line for writing the text

    # Get the size info from Pillow
    (textWidth, textHeight) = draw.multiline_textsize(text, font=font, spacing=spacing, stroke_width=strokeWidth)

    # Create a new image array large enough to hold the text, with a small margin on each side.
    textImageArray = newImageArray(textHeight+2*ymargin, textWidth+2*xmargin)

    # And set up another Pillow 'Draw' object, this time using the real target array.
    pilImage = Image.fromarray(textImageArray.astype('uint8'), 'RGB')
    draw = ImageDraw.Draw(pilImage, mode='RGBA')

    # And draw the rectangle into the image array, allowing for the small gap on each side.
    xy_topleft = (xmargin, ymargin)
    black = (0,0,0)
    draw.multiline_text(xy_topleft, text, font=font, fill=black, spacing=spacing, stroke_width=strokeWidth)

    # Generate a numpy 3-D array from image, as the object we return
    npa = np.array(pilImage)

    # Diagnostics to draw a back rectangle around the text, to aid in locating it in a finished image.
    addRectangle = False
    if addRectangle :
        from cv2 import cv2
        cv2.rectangle(npa, (0, 0, textWidth+2*xmargin, textHeight+2*ymargin), color=black, thickness=2 )

    # Diagnostic display of the image - NB this function gets called multiple times per run if there
    # are items detected by Rekognition.
    # showImage('PillowText', npa)   

    return npa

# #####################################################################################################

# Trial writing out text to an image using CV2 - not very nice looking. And no fixed-width font.
# Pillow works better, and also handles multi-line text itself.
# So the function below is not used, and not fully developed.

def addCV2Text(text) :
    from cv2 import cv2

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Work out how big we will need to make an array to display the text, line by line.
    lineCount = 0
    maxHeight = 0
    maxWidth = 0
    for line in enumerate(text.split('\n')):
        lineCount += 1
        s = line[1]
        (width, height), baseline = cv2.getTextSize(s, font, fontScale=1, thickness=2)
        print(height, width, baseline, s)
        maxHeight = max(maxHeight, height)
        maxWidth = max(maxWidth, width)

    textImgArray = newImageArray((maxHeight+20) * lineCount, maxWidth+20)

    print('Lines = ', lineCount)
    print('Maxh, Maxw =', maxHeight, maxWidth)
    print('Shape is', textImgArray.shape)

    # Line-by-line add the text to the array
    for line in enumerate(text.split('\n')):        # line is compound: (line-number, text)
        i = line[0]
        text_offset_x = 10
        text_offset_y = i * (maxHeight+20)
        cv2.putText(textImgArray, line[1], (text_offset_x, text_offset_y), font, fontScale=1, thickness=1, color=(0, 0, 0))

    showImage('CV2Text', textImgArray)

    return textImgArray

# #####################################################################################################

def addConfidenceScore(imgArraySource, confidenceText) :
    """ Add text in a bar added to the bottom of an image to show the confidence score and return 
        the new image. """

    # Work on a copy the original image.
    imgArray = imgArraySource.copy()

    # Generate an image containing the confidence text.
    textArray = getTextAsImageArray(confidenceText, fontPointSize=20, xmargin=0)
    # print('Adding conf to {0} {1} - {2}'.format(imgArray.shape, confidenceText, textArray.shape))

    # Add the text array at the bottom of the image, centred if the text array width is 
    # smaller than the width of the image.
    if textArray.shape[1] < imgArray.shape[1] :
        leftOffset = (imgArray.shape[1] - textArray.shape[1]) // 2
    else :
        leftOffset = 0
    imgArray = addImageAt(imgArray, textArray, imgArray.shape[0], leftOffset)

    return imgArray

# #####################################################################################################

def performImageExtraction(imgFile) :
    """ Invoke Rekognition on the image, return the response info and a text summary """

    # Use functions in the rt1 module to interact with Rekognition (including accessing local cache of
    # results if available.)
    labelsResponse = rt1.detectLabelsFromLocalFile(imgFile)
    summaryText = getSummaryText(imgFile, labelsResponse)
    return labelsResponse, summaryText

# #####################################################################################################

def produceOutputImage(imgFile, labelsResponse, summaryText) :

    imgArray = readImageArrayFromFile(imgFile)
    imgShape = imgArray.shape

    # print()
    # print('Image array type is {0}, shape is {1}'.format(type(imgArray), imgArray.shape))

    verticalSpacing = 50
    horizontalSpacing = 200

    a = np.full((imgShape[0] + verticalSpacing*2, imgShape[1] + horizontalSpacing*2, 3), 255, dtype='uint8')
    print("1:", a.shape)

    verticalStartPoint = verticalSpacing

    # Add the image to the array
    a = addImageAt(a, imgArray, verticalStartPoint, horizontalSpacing)
    verticalStartPoint += imgArray.shape[0] + verticalSpacing

    #showImage(imgFile, a)

    instancesInfo = rt1.extractInstancesInfo(imgArray, labelsResponse)

    textArray = getTextAsImageArray(summaryText)
    a = addImageAt( a, textArray, verticalStartPoint, horizontalSpacing)
    verticalStartPoint += textArray.shape[0] + verticalSpacing

    RGBColourGreen = (0, 255, 0)
    RGBColourYellow = (255, 255, 0)
    RGBColourMap = {
        'Person'    : RGBColourGreen,
        'Car'       : RGBColourYellow
    }

    if len(instancesInfo) > 0 :
        imgWithRectangles = addRectangleToImage(imgArray.copy(), instancesInfo, RGBColourMap)
        a = addImageAt(a, imgWithRectangles, verticalStartPoint, horizontalSpacing)
        verticalStartPoint += imgWithRectangles.shape[0] + verticalSpacing

        footer = np.full((verticalSpacing, a.shape[1], 3), 255, dtype='uint8')
        a = addImageAt(a, footer, verticalStartPoint, horizontalSpacing)
        verticalStartPoint += footer.shape[0]

        # Add a confidence number to each cropped image
        for info in instancesInfo :
            info['crop+conf'] = addConfidenceScore(info['crop'], info['conf_s'])

        # Add extracted images. Initially put each on a separate row, stop when out of room.
        # Should add some text to show label and confidence.
        horizontalRightLimit = horizontalSpacing + imgWithRectangles.shape[1]
        horizontalStartPoint = horizontalSpacing
        currentLabelName = ''
        rowHeight = 0
        spacingMultiple = 1

        for info in instancesInfo :
            crop = info['crop+conf']
            addLabel = False
            useNewRow = False

            if currentLabelName == '' :
                addLabel = True
                currentLabelName = info['labelname']

            if currentLabelName != info['labelname'] :
                addLabel = True
                currentLabelName = info['labelname']

            if horizontalStartPoint + crop.shape[1] >= horizontalRightLimit :
                useNewRow = True
                spacingMultiple = 1

            if addLabel or useNewRow:
                if addLabel :
                    print('Adding label', currentLabelName)
                    labelNameImage = getTextAsImageArray('Label = "{0}"'.format(currentLabelName))
                    verticalStartPoint += rowHeight + verticalSpacing * spacingMultiple
                    a = addImageAt(a, labelNameImage, verticalStartPoint, horizontalSpacing)
                    verticalStartPoint += labelNameImage.shape[0] + verticalSpacing * spacingMultiple
                    horizontalStartPoint = horizontalSpacing
                    rowHeight = 0
                else :
                    # Continuation of an existing label on another line
                    horizontalStartPoint = horizontalSpacing
                    verticalStartPoint += rowHeight + verticalSpacing * spacingMultiple
                    rowHeight = 0
                    currentLabelName = info['labelname']

            a = addImageAt(a, crop, verticalStartPoint, horizontalStartPoint)
            print('Added ', crop.shape, verticalStartPoint, horizontalStartPoint)
            rowHeight = max(rowHeight, crop.shape[0])
            horizontalStartPoint += crop.shape[1] + horizontalSpacing

        horizontalStartPoint = horizontalSpacing
        verticalStartPoint += rowHeight + verticalSpacing

    footer = np.full((verticalSpacing, a.shape[1], 3), 255, dtype='uint8')
    a = addImageAt(a, footer, verticalStartPoint, horizontalSpacing)

    writeImageArrayToFile('output.jpg', a)

# #####################################################################################################

def main(argv) :

    if len(argv) > 1 and argv[1] != '-' :
        imgFile = argv[1]
    else :
        imgFile = 'AI Services/woodbridge.jpg'
        print('No image file argument provided, using default : ', imgFile)

    if not os.path.isfile(imgFile) :
        print()
        print('*** File {0} not found'.format(imgFile))
        return

    (labelsResponse, summaryText) = performImageExtraction(imgFile)

    print()
    print(summaryText)
    print()

    produceOutputImage(imgFile, labelsResponse, summaryText)

# #####################################################################################################

if __name__ == '__main__' :    
    main(sys.argv)