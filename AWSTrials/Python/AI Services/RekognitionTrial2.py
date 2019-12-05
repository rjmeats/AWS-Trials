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
# - colour, as three separate values, for R,G,B
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

# CV2 version - not used
def writeImageArrayToFileUsingCV2(filename, imgArray) :

    from cv2 import cv2
    cv2.imwrite(filename, convertToBGR(imgArray))
    print('Image file saved: {0}'.format(filename))

# Diagnostics function, to see intermediate images during development. The Window remains open until you
# press a key.

def show(title, imgArray) :
    """ Display an image in a CV2 window """

    # For CV2 we need to reverse the colour ordering of the array to BGR
    from cv2 import cv2
    cv2.imshow(title, convertToBGR(imgArray.copy()))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# #####################################################################################################

def convertToBGR(imgArray) :
    """ Converts a 3-D [y,x,RGB] numpy array to [y,x,BGR] format, for use with CV2 """
    return imgArray[:,:,::-1]

# #####################################################################################################

def getSummaryText(imgFile, labelsResponse) :

    from io import StringIO

    temp_out = StringIO()
    current_out = sys.stdout
    sys.stdout = temp_out
    rt1.dumpLabelInfo(imgFile, labelsResponse)
    sys.stdout = current_out
    return temp_out.getvalue()

# #####################################################################################################

def extendImage(a, newy, newx) :
    newa = np.full((newy, newx,3), 255, dtype='uint8')
    newa[0:a.shape[0],0:a.shape[1]] = a[:,:]
    print('Extended array of shape {0} to a new array of shape {1}'.format(a.shape, newa.shape))
    return newa

def addImageAt(top, left, amain, a) :
    print('Adding image of shape {0} to image of shape {1} at point ({2},{3})'.format(
            a.shape, amain.shape, top, left))
    # Check sizes and extend if necessary ?
    if top + a.shape[0] > amain.shape[0] :
        print('Need to extend down')
        # Need to extend vertically
        amain = extendImage(amain, top + a.shape[0], amain.shape[1])
        print('New shape is {0}'.format(amain.shape))

    if left + a.shape[1] > amain.shape[1] :
        print('Need to extend right')
        # Need to extend horizontally
        amain = extendImage(amain, amain.shape[0], left + a.shape[1])
        print('New shape is {0}'.format(amain.shape))

    amain[top:top+a.shape[0],left:left+a.shape[1]] = a[:,:]
    return amain

# #####################################################################################################

def addRectanglesToImage(img, instancesInfo) :
    from cv2 import cv2
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

# #####################################################################################################

def addConf(a, conf_s) :
    a2 = a.copy()
    textArray = getPillowText(conf_s)
    print('Adding conf to {0} {1} - {2}'.format(a2.shape, conf_s, textArray.shape))
    if textArray.shape[1] >= a2.shape[1] :
        centreOffset = 0
    else :
        centreOffset = (a2.shape[1] - textArray.shape[1])//2

    a2 = addImageAt(a2.shape[0], centreOffset, a2, textArray)
    #show('conf', a2)
    return a2

# #####################################################################################################

def addCV2Text(a, summary) :
    from cv2 import cv2
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

# #####################################################################################################

def getPillowText(summary) :

    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype("cour.ttf", 25)

    dummyArray = np.full((100, 100, 3), 255, dtype='uint8')

    pilImage = Image.fromarray(dummyArray.astype('uint8'), 'RGB')
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
        from cv2 import cv2
        cv2.rectangle(npa, (0, 0, textwidth+2*gap, textheight+2*gap), color=(0,0,0), thickness=2 )

    #show('PillowText', npa)

    return npa

# #####################################################################################################

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

    if not os.path.isfile(imgFile) :
        print()
        print('*** File {0} not found'.format(imgFile))
        return

    # Process the image file
    labelsResponse = rt1.detectLabelsFromLocalFile(imgFile)
    summary = getSummaryText(imgFile, labelsResponse)
    print()
    print(summary)
    print()
    rt1.dumpLabelInfo(imgFile, labelsResponse)

    imgArray = readImageArrayFromFile(imgFile)
    imgShape = imgArray.shape

    print()
    print('Image array type is {0}, shape is {1}'.format(type(imgArray), imgArray.shape))

    verticalSpacing = 50
    horizontalSpacing = 200

    a = np.full((imgShape[0] + verticalSpacing*2, imgShape[1] + horizontalSpacing*2, 3), 255, dtype='uint8')
    print("1:", a.shape)

    verticalStartPoint = verticalSpacing

    # Add the image to the array
    a = addImageAt(verticalStartPoint, horizontalSpacing, a, imgArray)
    verticalStartPoint += imgArray.shape[0] + verticalSpacing

    #show(imgFile, a)

    instancesInfo = rt1.extractInstancesInfo(imgArray, labelsResponse)

    textArray = getPillowText(summary)
    a = addImageAt(verticalStartPoint, horizontalSpacing, a, textArray)
    verticalStartPoint += textArray.shape[0] + verticalSpacing

    if len(instancesInfo) > 0 :
        imgWithRectangles = addRectanglesToImage(imgArray.copy(), instancesInfo)
        a = addImageAt(verticalStartPoint, horizontalSpacing, a, imgWithRectangles)
        verticalStartPoint += imgWithRectangles.shape[0] + verticalSpacing

        footer = np.full((verticalSpacing, a.shape[1], 3), 255, dtype='uint8')
        a = addImageAt(verticalStartPoint, horizontalSpacing, a, footer)
        verticalStartPoint += footer.shape[0]

        # Add a confidence number to each cropped image
        for info in instancesInfo :
            info['crop+conf'] = addConf(info['crop'], info['conf_s'])

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
                    labelNameImage = getPillowText('Label = "{0}"'.format(currentLabelName))
                    verticalStartPoint += rowHeight + verticalSpacing * spacingMultiple
                    a = addImageAt(verticalStartPoint, horizontalSpacing, a, labelNameImage)
                    verticalStartPoint += labelNameImage.shape[0] + verticalSpacing * spacingMultiple
                    horizontalStartPoint = horizontalSpacing
                    rowHeight = 0
                else :
                    # Continuation of an existing label on another line
                    horizontalStartPoint = horizontalSpacing
                    verticalStartPoint += rowHeight + verticalSpacing * spacingMultiple
                    rowHeight = 0
                    currentLabelName = info['labelname']

            a = addImageAt(verticalStartPoint, horizontalStartPoint, a, crop)
            print('Added ', crop.shape, verticalStartPoint, horizontalStartPoint)
            rowHeight = max(rowHeight, crop.shape[0])
            horizontalStartPoint += crop.shape[1] + horizontalSpacing

        horizontalStartPoint = horizontalSpacing
        verticalStartPoint += rowHeight + verticalSpacing

    footer = np.full((verticalSpacing, a.shape[1], 3), 255, dtype='uint8')
    a = addImageAt(verticalStartPoint, horizontalSpacing, a, footer)


    writeImageArrayToFile('output.jpg', a)
    #writeImageArrayToFileUsingCV2('output2.jpg', a)

# #####################################################################################################

if __name__ == '__main__' :    
    main(sys.argv)