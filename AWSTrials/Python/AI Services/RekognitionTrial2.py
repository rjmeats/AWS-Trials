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

def addRectanglesToImage(imgArray, instanceInfo, RGBColourMap) :
    """ Use 'instance info' obtained from Rekognition to draw rectangles in the specified colour around 
        the labelled instances located in the main image. """

    # Use CV2 for this. NB We specify colours as RGB, as that is what we're using for the array. But if we
    # ever used CV2's colours, they would be BGR and so need reversing to match the rest of the array.
    from cv2 import cv2

    # Potential CV2 aLpha handling if ever required
    # https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c

    RGBColourWhite = (255, 255, 255)
    unknownLabelColour = RGBColourMap.get('Unknown', RGBColourWhite)

    for info in instanceInfo :        
        RGBColour = RGBColourMap.get(info['labelname'], unknownLabelColour)
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

# Define a mapping between Rekognition label types and the colour of rectangle we draw around the item.
RGBColourGreen = (0,255,0)
RGBColourYellow = (255,255,0)
RGBColourWhite = (255,255,255)
RGBColourMap = {
    'Person'    : RGBColourGreen,
    'Car'       : RGBColourYellow,
    'Unknown'   : RGBColourWhite
}

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

def generateRowImageArray(rowImages, horizontalSpacing) :
    """ Places the images into a single row image, with the specified spacing. """

    # Work out the height that the combined image needs to be
    rowHeight = max([image.shape[0] for image in rowImages])

    # Initial array dimensions don't really matter (as long as not too large), we will extend as we
    # go along.
    rowImage = newImageArray(rowHeight, horizontalSpacing)
    horizontalOffset = 0
    for image in rowImages :
        rowImage = addImageAt(rowImage, image, 0, horizontalOffset)
        #rowImage = addImageAt(rowImage, image, rowHeight - image.shape[0], horizontalOffset)
        horizontalOffset += horizontalSpacing + image.shape[1]
    
    return rowImage

def layoutExtractedImages(instances, maxRowWidth, horizontalSpacing) :
    """ Lays out the set of instances in rows, returning a list of rows. """

    # Return the set of rows found as a list.
    rows = []

    # Build up the set of images to display on each row in turn, until the row width
    # has been used up, then start a new row.
    rowImages = []
    rowWidth = 0
    for instance in instances :
        # Add confidence score text below each cropped image
        imgCroppedArray = addConfidenceScore(instance['crop'], instance['conf_s'])
        imgWidth = imgCroppedArray.shape[1]
        # Will this instance fit into the current row ? Always put at least one item in.
        if len(rowImages) == 0:
            rowImages.append(imgCroppedArray)
            rowWidth = imgWidth
        elif rowWidth + horizontalSpacing + imgWidth <= maxRowWidth :
            rowImages.append(imgCroppedArray)
            rowWidth += horizontalSpacing + imgWidth
        else :
            # No more for this row. Create an overall image for the items in the row.
            rows.append(generateRowImageArray(rowImages, horizontalSpacing))
            # Put the current item at the start of a new row.
            rowImages.clear()
            rowImages.append(imgCroppedArray)
            rowWidth = imgWidth

    # Deal with the final row.
    if len(rowImages) > 0 :
        rows.append(generateRowImageArray(rowImages, horizontalSpacing))

    return rows

# #####################################################################################################

def performLabelExtraction(imgFile) :
    """ Invoke Rekognition on the image, return the response info and a text summary """

    # Use functions in the rt1 module to interact with Rekognition (including accessing local cache of
    # results if available.)
    labelsResponse = rt1.detectLabelsFromLocalFile(imgFile)
    summaryText = getSummaryText(imgFile, labelsResponse) 
    summaryText = summaryText.rstrip()  # Remove trailing whitespace, especially newlines
    return labelsResponse, summaryText

# #####################################################################################################

def produceOutputImage(imgFile, labelsResponse, summaryText, outputFileName) :
    """ Does all the processing of the source image and Rekognition label data to produce the output image """

    # Get the image we're processing into a 3-D numpy array [y,x,RGB]
    imgSourceArray = readImageArrayFromFile(imgFile)
    sourceShape = imgSourceArray.shape

    # print()
    # print('Image array type is {0}, shape is {1}'.format(type(imgSourceArray), sourceShape))

    # Set up an all-white image array to use as a vertical spacing element at various points
    horizontalMargin = 100
    verticalMargin = 50
    verticalSpacingArray = newImageArray(verticalMargin, sourceShape[1]+2*horizontalMargin)

    # Use the 'imgTargetArray' variable to reference the array for output image being built up.

    # Start by putting a margin at the top
    imgTargetArray = verticalSpacingArray.copy()      

    # Add the source image, and a vertical spacing element
    imgTargetArray = addImageAt(imgTargetArray, imgSourceArray, imgTargetArray.shape[0], horizontalMargin)
    imgTargetArray = addImageAt(imgTargetArray, verticalSpacingArray, imgTargetArray.shape[0], 0)

    # showImage(imgFile, imgTargetArray)

    # Now move onto the Rekognition data
    # Reformat the data a little
    instancesInfo = rt1.extractInstancesInfo(imgSourceArray, labelsResponse)

    # Put the multi-line text summarising the Rekognition labels detected into image form.
    textArray = getTextAsImageArray(summaryText)    

    # Add whitespace margin to the right of the text array if it is wider than the main image.
    if textArray.shape[1] > sourceShape[1] :
        textArray = extendImage(textArray, textArray.shape[0], textArray.shape[1] + horizontalMargin)

    # Add the image-ised text to the bottom for the output image, and a vertical spacing element
    imgTargetArray = addImageAt(imgTargetArray, textArray, imgTargetArray.shape[0], horizontalMargin)
    imgTargetArray = addImageAt(imgTargetArray, verticalSpacingArray, imgTargetArray.shape[0], 0)

    # showImage(imgFile, imgTargetArray)

    # If Rekognition detected any labelled items in the source image, add another copy of the source image, 
    # this time with coloured rectangles drawn on it to show where the labelled items are.
    if len(instancesInfo) > 0 :
        imgWithRectangles = addRectanglesToImage(imgSourceArray.copy(), instancesInfo, RGBColourMap)
        imgTargetArray = addImageAt(imgTargetArray, imgWithRectangles, imgTargetArray.shape[0], horizontalMargin)

    # And now add the individual extracted images (showing confidence values) grouped by label type,
    # with multiple images per row.
    if len(instancesInfo) > 0 :
        # Use reduced vertical spacing element between items here.
        verticalRowSpacingArray = newImageArray(verticalMargin // 2, imgTargetArray.shape[1])

        # Go through each distinct label type in turn
        labelNames = sorted(set(instance['labelname'] for instance in instancesInfo), reverse=False)
        for labelName in labelNames :
            # Add the label name text as a section heading
            imgLabelName = getTextAsImageArray('Label = "{0}"'.format(labelName))
            imgTargetArray = addImageAt(imgTargetArray, verticalSpacingArray, imgTargetArray.shape[0], 0)
            imgTargetArray = addImageAt(imgTargetArray, imgLabelName, imgTargetArray.shape[0], horizontalMargin)

            # Display images with this label name, spaced out into multiple rows if necessary.
            instances = [ instance for instance in instancesInfo if instance['labelname'] == labelName ]
            availableWidth = imgTargetArray.shape[1] - 2*horizontalMargin
            rowsOfImages = layoutExtractedImages(instances, availableWidth, horizontalMargin)
            for imgOfRowOfImages in rowsOfImages :
                imgTargetArray = addImageAt(imgTargetArray, verticalRowSpacingArray, imgTargetArray.shape[0], 0)
                imgTargetArray = addImageAt(imgTargetArray, imgOfRowOfImages, imgTargetArray.shape[0], horizontalMargin)

    # Add a final spacing element at the bottom, and write the final image to a file.
    imgTargetArray = addImageAt(imgTargetArray, verticalSpacingArray, imgTargetArray.shape[0], 0)
    writeImageArrayToFile(outputFileName, imgTargetArray)

    return

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

    if len(argv) > 2 :
        outputFileName = argv[2]
    else :
        outputFileName = 'output.jpg'
        print('No output file provided, using default : ', outputFileName)

    (labelsResponse, summaryText) = performLabelExtraction(imgFile)

    print()
    print(summaryText)
    print()

    produceOutputImage(imgFile, labelsResponse, summaryText, outputFileName)

# #####################################################################################################

if __name__ == '__main__' :    
    main(sys.argv)