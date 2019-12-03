# Read a local image file, send it to the Amazon Rekognition API to extract a set of items
# found in the image, and then manipulate the image to indicate what was found and where.
#
# https://docs.aws.amazon.com/rekognition/latest/dg/
#
# Does this with three different Python image-processing tools to see how they work.
# - MatPlotLib
# - Pillow
# - OpenCV

import sys
import os

import numpy as np      
import boto3            # Python interface to AWS
import pickle           # To save Rekognition response in a simple local cache
import pprint           # Dump Python data structure showing the Rekognition response in a readable format

# #####################################################################################################

# Invoke Rekognition, via Boto3, to extract 'labels' from an image in a specified file. Responses are
# cached locally to avoid repeated calls to Rekognition for the same image file:
# - mainly for speed, avoids the time taken uploading the image to Rekognition each time, as well as
#   Rekognition processing time
# - also avoids some AWS charging for Rekognition use

def detectLabelsFromLocalFile(imgFile) :
    """ Return Rekognition label data (in Boto3 form) extracted from the specified image file. """

    # Check for a cached response file. The cached response will be in a cache folder, with the cached
    # file name derived from the image file name = NB the current simple scheme doesn't work when different
    # images have the same file name! Also, doesn't clear the cache ever, or put a time limit on entries,
    # so not operationally robust.

    imgFileBasename = os.path.basename(imgFile)

    # Use cache folder specified in environment, if present, otherwise a default.
    envVarName = 'REKOGNITION_RESPONSE_CACHE_LOCATION'
    cacheDefault = os.path.join(os.path.dirname(__file__), 'responsesCache')
    cacheLocation = os.environ.get(envVarName, cacheDefault)

    # We cache two files per image: a 'pickle' format data structure, and a human-readable form of the same data
    cacheFile = os.path.join(cacheLocation, imgFileBasename + '.response')
    prettyCacheFile = os.path.join(cacheLocation, imgFileBasename + '.response.pretty.txt')

    if os.path.isfile(cacheFile) :
        print('Cache file {0} found ..'.format(cacheFile))

        with open(cacheFile, 'rb') as f:
            response = pickle.load(f)
            print('.. read pre-existing response from cache file')
    else :
        print('No cache file {0} found, invoking Rekognition ..'.format(cacheFile))

        # Use boto3 to make the Rekognition 'detect labels' call, passing in the image as 
        # bytes (which Boto3 presumably converts to base-64 encoding).
        client = boto3.client('rekognition')
        with open(imgFile, 'rb') as image :
            response = client.detect_labels(Image={'Bytes' : image.read() })
            print('.. read response from Rekognition')

        # Boto3 converts the raw Rekognition HTTP response to a Python data structure. Use pickle to
        # cache this data.
        with open(cacheFile, 'wb') as f:
            pickle.dump(response, f)
            print('Written Rekognition response as binary object to cache file {0}'.format(cacheFile))

    # Produce a human-readable version of the Rekognition+Boto3 response data structure, and cache this too.
    pp = pprint.PrettyPrinter(indent=4)
    pstring = pp.pformat(response)
    with open(prettyCacheFile, 'w') as f:
        f.write(pstring)
        print('Dumped formatted response to file {0}'.format(prettyCacheFile))

    return response

# #####################################################################################################

def dumpLabelInfo(imgFile, labelsResponse) :
    """ Print out basic info about the image file and the Rekognition labels found in it """

    import matplotlib.image as mpimg 
    img = mpimg.imread(imgFile)

    print()
    print('File size: {0} bytes'.format(os.path.getsize(imgFile)))
    print('Image dimensions v x h: {0} x {1}'.format(img.shape[0], img.shape[1]))
    print()
    print('Labels found in {0}:'.format(imgFile))
    print()
    for label in labelsResponse['Labels'] :
        parents = ', '.join([ d['Name'] for d in label['Parents'] ])
        conf_s = '{0:.1f}'.format(label['Confidence'])
        # 'Instances' are cases where Rekognition provides a bounding box.
        instanceCount = len(label['Instances'])
        print('{0:20.20s} {1}   instances = {2:2d}   parents = {3}'.format(label['Name'], conf_s, instanceCount, parents))

# #####################################################################################################

def extractInstancesInfo(img, labelsResponse) :
    """ Extract into a list the basic info about all the 'instances' reported by Rekognition in the image """

    verticalSize, horizontalSize = img.shape[0], img.shape[1]
    extractions = []

    for label in labelsResponse['Labels']:
        instances = label['Instances']
        for instance in instances :
            info = {}
            info['labelname'] = label['Name']
            info['conf'] = instance['Confidence']
            info['conf_s'] = '{0:.1f}'.format(instance['Confidence'])
            box = instance['BoundingBox']
            info['height'] = int(box['Height'] * verticalSize)
            info['width'] = int(box['Width'] * horizontalSize)
            info['topoffset'] = int(box['Top'] *verticalSize)
            info['bottomoffset'] = info['topoffset'] + info['height']
            info['leftoffset'] = int(box['Left'] * horizontalSize)
            info['rightoffset'] = info['leftoffset'] + info['width']
            info['crop'] = img[
                    info['topoffset']:info['bottomoffset'],
                    info['leftoffset']:info['rightoffset'],
                    :]
            extractions.append(info)

    return extractions

# #####################################################################################################

def displayImageWithMatPlotLib(imgFile, labelsResponse) :
    """ Display the image and identified items within it, using the MatPlotLib library """

    import matplotlib.image as mpimg 

    # Read in the image, with MatPlotLib providing a 3-D numpy array
    # Dimensions of the numpy array are:
    # - y axis, moving down from the top of the image to the bottom
    # - x axis, moving from the left side of the image to right
    # - colour, as three separate values, for R,G,B
    img = mpimg.imread(imgFile) 

    print()
    print('Displaying using MatPlotLib, image type is {0}, shape is {1}'.format(type(img), img.shape))
    #print(img[0,0,0], img[0,0,1], img[0,0,2])

    # Pull out the info from the response relating to instances found within the image, and plot them
    # using MatPlotLib
    instancesInfo = extractInstancesInfo(img, labelsResponse)
    drawMatPlotLib(img.copy(), instancesInfo)
    
def drawMatPlotLib(img, instancesInfo) :
    """ Do the actual MatPlotLib display work """

    import matplotlib.pyplot as plt 
    patches = []
    items = []
    for info in instancesInfo :
        boxc = 'red' if info['labelname'] == 'Person' else 'green'
        # Plot a box on the image at the appropriate point. NB the drawn border of the rectangle straddles the actual border when 
        # using larger line widths, not clear if this can be controlled to plot the rectangle entirely within/without the area.
        # NB units of line width seem to stay fixed as picture is enlarged, so not just being applied as pixel changes to the image.
        # Some more info at https://stackoverflow.com/questions/30081846/set-matplotlib-rectangle-edge-to-outside-of-specified-width

        #patches.append(plt.Rectangle((info['leftoffset']-0.25, info['topoffset']-0.25), info['width']+0.5, info['height']+0.5, 
        #                    edgecolor='yellow', alpha=0.4, lw=1,facecolor='none'))
        patches.append(plt.Rectangle((info['leftoffset'], info['topoffset']), info['width'], info['height'], 
                            edgecolor=boxc, alpha=0.8, lw=1,facecolor='none'))

        if len(items) < 20 :
            items.append((info['crop'], info['labelname'], info['conf_s']))
        else :
            print('Too many items to display - ignoring', info['labelname'])

    # Very rough attempt to show main image and then images of identified items on one plot. 
    # Could be laid out much better, and scaled better.
    colSetting = len(items)
    if colSetting < 6 :
        colSetting = 6
    rowSetting = 6
    fig = plt.figure(figsize=(colSetting, rowSetting))
    gridy = len(items)
    if gridy == 0 :
        gridy = 1
    grid = plt.GridSpec(4, gridy, hspace=1.2)
    
    # Show main image
    main_ax = fig.add_subplot(grid[0:3, :])
    for patch in patches :
        main_ax.add_patch(patch)
    main_ax.imshow(img)

    # Show the items found as small sub-images
    for i in range(0, len(items)) :
        sub_ax = fig.add_subplot(grid[3,i])
        sub_ax.imshow(items[i-1][0])
        sub_ax.set_title(items[i-1][1] + ' (' + items[i-1][2] + ')')
        sub_ax.set_yticklabels([])
        sub_ax.set_xticklabels([])
    plt.show()

# #####################################################################################################

def displayImageWithPillow(imgFile, labelsResponse) :
    """ Display the image and identified items within it, using the Pillow library """

    # https://pillow.readthedocs.io/en/stable/

    from PIL import Image

    img = Image.open(imgFile) 

    print()
    print('Displaying using Pillow, image type is {0}, size is {1}'.format(type(img), img.size))
    # Pillow produces an image object which is its own JpegImageFile type.
    # Produce a numpy array from it as follows:
    npa = np.array(img)
    #print(type(npa), npa.shape, img.size)
    #print(npa[0,0,0], npa[0,0,1], npa[0,0,2])
    # The numpy array dimensions are: 
    # - y axis, moving down from the top of the image to the bottom
    # - x axis, moving from the left side of the image to right
    # - colour, as three separate values, for R,G,B
    # NB img.size (pillow) and npa.shape (numpy) have the y and x axes the opposite way round, so the
    # production of the numpy array seems to switch over the y and x axes so that they are the same
    # orientation as the direct numpy arrays produced by matplotlib and OpenCV2.

    # Pull out the info from the response relating to instances found within the image, and plot them
    # using Pillow
    instancesInfo = extractInstancesInfo(npa, labelsResponse)
    drawPillow(npa, instancesInfo)

def drawPillow(img, instancesInfo) :
    """ Do the actual Pillow display work """

    from PIL import Image, ImageDraw, ImageColor

    # Recreate the image as a Pillow image object from the numpy RGB image
    pilImage = Image.fromarray(img.astype('uint8'), 'RGB')

    draw = ImageDraw.Draw(pilImage, mode='RGBA')
    croppedImages = []
    for info in instancesInfo :
        # Draw rectangles on the main image
        boxc = 'red' if info['labelname'] == 'Person' else 'green'
        rect = (info['leftoffset'],info['topoffset'], info['rightoffset'], info['bottomoffset'])
        alpha = 200
        colour = (*ImageColor.getrgb(boxc), alpha)
        draw.rectangle(rect, fill=None, outline=colour, width=2)

        # Produced a separate cropped image for each item extracted.
        croppedImage = Image.fromarray(info['crop'].astype('uint8'), 'RGB')
        croppedDraw = ImageDraw.Draw(croppedImage, mode='RGBA')
        # Write a title onto the cropped image
        croppedDraw.text((0,0), info['labelname'] + ' (' + info['conf_s'] + ')')
        croppedImages.append(croppedImage)

    # Show the main image with added rectangles
    pilImage.show()

    # Show the first few extracted images. NB Pillow's 'show' opens a new window for each, which
    # need to be manually closed one-by-one, so don't do too many of them.
    for croppedImage in croppedImages[0:3] :
        croppedImage.show()
# 

# #####################################################################################################

def displayImageWithOpenCV(imgFile, labelsResponse) :
    """ Display the image and identified items within it, using the OpenCV library """
    
    from cv2 import cv2     # NB pylint shows warnings about not finding cv2 members if we do
                            # just 'import cv2' - https://github.com/PyCQA/pylint/issues/2426

    # Read in the image, with MatPlotLib providing a 3-D numpy array
    # Dimensions of the numpy array are:
    # - y axis, moving down from the top of the image to the bottom
    # - x axis, moving from the left side of the image to right
    # - colour, as three separate values, for B,G,R - NB the reverse order compared to MatPlotLib
    img = cv2.imread(imgFile)

    print()
    print('Displaying using OpenCV, image type is {0}, shape is {1}'.format(type(img), img.shape))
    #print(img[0,0,0], img[0,0,1], img[0,0,2])

    # Pull out the info from the response relating to instances found within the image, and plot them
    # using MatPlotLib
    instancesInfo = extractInstancesInfo(img, labelsResponse)
    drawCV2(img.copy(), instancesInfo)
    
# #####################################################################################################

def drawCV2(img, instancesInfo) :
    """ Do the actual CV2 display work """

    # https://docs.opencv.org/master/index.html
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    #  - NB old version https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html#rectangle

    from cv2 import cv2

    # Potential aLpha handling
    # https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
    bgrcolorRed = (0, 0, 255)
    bgrcolorGreen = (0, 255, 0)
    #bgrcolorYellow = (0, 255, 255)

    for info in instancesInfo :
        boxc = bgrcolorRed if info['labelname'] == 'Person' else bgrcolorGreen
        cv2.rectangle(img, (info['leftoffset'], info['topoffset'], info['width'], info['height']), color=boxc, thickness=2 )
        #cv2.rectangle(img, (info['leftoffset']-1, info['topoffset']-1, info['width']+2, info['height']+2), color=bgrcolorYellow, thickness=1 )

    # For large images, this produces a window filling the screen but only showing a small part of the whole,
    # and no obvious way to scroll around.
    cv2.imshow('image', img)

    # Displays each item in its own window, same size as in original, but with annoying grey to create a minimum
    # window size. Needs to have a unique window name for each one, or just superimpose.
    # Needs more work!
    n = 0
    for info in instancesInfo:
        windowName = 'I_' + str(n) + ' ' + info['labelname'] + ' ' + info['conf_s']
        n += 1
        cv2.imshow(windowName, info['crop'])

    # # Keep windoes open until a key is pressed, while any of the Windows is in focus.
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    # Process the image file
    labelsResponse = detectLabelsFromLocalFile(imgFile)
    dumpLabelInfo(imgFile, labelsResponse)

    # Display the image and the identified items in it
    if tool.upper() == 'MatPlotLib'.upper() :
        displayImageWithMatPlotLib(imgFile, labelsResponse)
    elif tool.upper() == 'Pillow'.upper() :
        displayImageWithPillow(imgFile, labelsResponse)
    elif tool.upper() == 'OpenCV'.upper() or tool.upper() == 'CV2'.upper() :
        displayImageWithOpenCV(imgFile, labelsResponse)
    elif tool == '-' :
        print()
        print('No display option specified')
    else :
        print()
        print('Unknown display tool:', tool)

if __name__ == '__main__' :    
    main(sys.argv)
