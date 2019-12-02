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
        parents = ", ".join([ d['Name'] for d in label['Parents'] ])
        conf_s = "{0:.1f}".format(label['Confidence'])
        instanceCount = len(label['Instances'])
        print("{0:20.20s} {1}   instances = {2:2d}   parents = {3}".format(label['Name'], conf_s, instanceCount, parents))

# #####################################################################################################

def displayImageWithMatPlotLib(imgFile, labelsResponse) :

# https://www.geeksforgeeks.org/reading-images-in-python/

    import matplotlib.image as mpimg 
    import matplotlib.pyplot as plt 

    img = mpimg.imread(imgFile) 

    #Fetching imaging size info from plot. But realised can get from image object more directly
    #verticalSize = abs(ax.get_ybound()[1] - ax.get_ybound()[0])
    #horizontalSize = abs(ax.get_xbound()[1] - ax.get_xbound()[0])

    verticalSize, horizontalSize, dummy = img.shape

    print()
    print('Displaying using MatPlotLib, image type is {0}, shape is {1}'.format(type(img), img.shape))

    #labels = responseData['Labels']
    patches = []
    labels = labelsResponse['Labels']
    items = []
    for label in labels:
        instances = label['Instances']
        conf_s = "{0:.1f}".format(label['Confidence'])
        if label['Name'] == "Person" :
            boxc = 'red'
        elif len(instances):
            boxc = 'green'

        for instance in instances :
            conf_s = "{0:.1f}".format(instance['Confidence'])
            box = instance['BoundingBox']
            boxheight = int(box['Height'] * verticalSize)
            boxwidth = int(box['Width'] * horizontalSize)
            topoffset = int(box['Top'] *verticalSize)
            leftoffset = int(box['Left'] * horizontalSize)
            # Plot a box on the image at the appropriate point. NB line of rectangle is outside selected area (unlike cv2)
            #ax.add_patch(plt.Rectangle((leftoffset, topoffset), boxwidth, boxheight, edgecolor=boxc, alpha=0.5, lw=1,facecolor='none'))
            patches.append(plt.Rectangle((leftoffset, topoffset), boxwidth, boxheight, edgecolor=boxc, alpha=0.5, lw=4,facecolor='none'))

            # Pull out the part of the image that contains the item into a separate small image.
            rectImg = img[topoffset:topoffset+boxheight,leftoffset:leftoffset+boxwidth,:]
            #print(rectImg.shape)
            if len(items) < 20 :
                items.append((rectImg, label['Name'], conf_s))
            else :
                print("Too many items to display - ignoring", label['Name'])

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
        sub_ax.set_title(items[i-1][1] + " (" + items[i-1][2] + ")")
        sub_ax.set_yticklabels([])
        sub_ax.set_xticklabels([])
    plt.show()

def displayImageWithPillow(imgFile, labelsResponse) :

# https://www.geeksforgeeks.org/reading-images-in-python/
# https://pillow.readthedocs.io/en/stable/

    from PIL import Image, ImageDraw, ImageColor

    img = Image.open(imgFile) 

    print()
    print('Displaying using Pillow, image type is {0}, size is {1}'.format(type(img), img.size))
    # Convert the image to a numpy array as follows
    npa = np.array(img)
    print(type(npa), npa.shape)

    horizontalSize, verticalSize = img.size   # (x,y) NB Opposite way round from matplotlib

    labels = labelsResponse['Labels']
    rects = []
    items = []
    for label in labels:
        instances = label['Instances']
        conf_s = "{0:.1f}".format(label['Confidence'])
        if label['Name'] == "Person" :
            boxc = 'red'
        elif len(instances):
            boxc = 'green'

        for instance in instances :
            conf_s = "{0:.1f}".format(instance['Confidence'])
            box = instance['BoundingBox']
            boxheight = int(box['Height'] * verticalSize)
            boxwidth = int(box['Width'] * horizontalSize)
            topoffset = int(box['Top'] *verticalSize)
            leftoffset = int(box['Left'] * horizontalSize)

            rect = leftoffset,topoffset, leftoffset+boxwidth, topoffset+boxheight
            rects.append((rect, boxc))

            crop = img.crop(rect)
            draw = ImageDraw.Draw(crop, mode='RGBA')
            draw.text((0,0), label['Name'] + " (" + conf_s + ")")

            items.append(crop)

            # if len(items) < 20 :
            #     items.append((rectImg, label['Name']))
            # else :
            #     print("Too many items to display - ignoring", label['Name'])


    # print(type(img))
    # print(img.format)     
    # print(img.mode) 
    # print(img.size) 

    draw = ImageDraw.Draw(img, mode='RGBA')
    for rect in rects :
        alpha = 80
        colour = (*ImageColor.getrgb(rect[1]),alpha)
        draw.rectangle(rect[0], fill=None, outline=colour, width=5)

    img.show() 

    # Displays each item on its own image page. Not clear how size of displayed image is determined.
    # Pillow just invokes the Windows application assigned to .png files, so doesn't control size.
    # Needs more work!
    for item in items[0:6]:
        item.show()

# https://docs.opencv.org/master/index.html
# https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
#  - NB old version https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html#rectangle

# 

def displayImageWithOpenCV(imgFile, labelsResponse) :
    # NB pylint is showing warnings about not finding cv2 members - https://github.com/PyCQA/pylint/issues/2426
    # if do just 'import cv2'
    from cv2 import cv2
    img = cv2.imread(imgFile)

    print()
    print('Displaying using OpenCV, image type is {0}, shape is {1}'.format(type(img), img.shape))

    # Potential aLpha handling
    # https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
    bgrcolorRed = (0, 0, 255)
    bgrcolorGreen = (0, 255, 0)

    verticalSize, horizontalSize, dummy = img.shape

    labels = labelsResponse['Labels']
    rects = []
    items = []
    for label in labels:
        instances = label['Instances']
        conf_s = "{0:.1f}".format(label['Confidence'])
        if label['Name'] == "Person" :
            boxc = bgrcolorRed
        elif len(instances):
            boxc = bgrcolorGreen
        for instance in instances :
            conf_s = "{0:.1f}".format(instance['Confidence'])
            box = instance['BoundingBox']
            boxheight = int(box['Height'] * verticalSize)
            boxwidth = int(box['Width'] * horizontalSize)
            topoffset = int(box['Top'] *verticalSize)
            leftoffset = int(box['Left'] * horizontalSize)

            rect = leftoffset,topoffset, boxwidth, boxheight
            rects.append((rect, boxc))

            rectImg = img[topoffset:topoffset+boxheight,leftoffset:leftoffset+boxwidth,:].copy()
            #draw = ImageDraw.Draw(crop, mode='RGBA')
            #draw.text((0,0), label['Name'] + "(" + conf_s + ")")
            items.append((rectImg, label['Name'], conf_s))

    for rect in rects :
        cv2.rectangle(img, rect[0], rect[1], thickness=1)

    # For large images, this produces a window filling the screen but only showing a small part of the whole,
    # and no obvious way to scroll around.
    cv2.imshow('image', img)

    # Displays each item in its own window, same size as in original, but with annoying grey to create a minimum
    # window size. Needs to have a unique window name for each one, or just superimpose.
    # Needs more work!
    n = 0
    for item in items:
        windowName = 'I_' + str(n) + " " + item[1] + " " + item[2]
        n += 1
        cv2.imshow(windowName, item[0])

    # Keep windoes open until a key is pressed, while any of the Windows is in focus.
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(argv) :

    if len(argv) > 1 and argv[1] != '-' :
        imgFile = argv[1]
    else :
        imgFile = 'AI Services/woodbridge.jpg'
        print("No image file argument provided, using default : ", imgFile)

    if len(argv) > 2 :
        tool = argv[2]
    else :
        tool = 'MatPlotLib'
        print("No tool argument provided, using default : ", tool)

    # Process the image file
    labelsResponse = detectLabelsFromLocalFile(imgFile)
    dumpLabelInfo(imgFile, labelsResponse)

    # Display the image and the identified items in it
    if tool.upper() == 'MatPlotLib'.upper() :
        displayImageWithMatPlotLib(imgFile, labelsResponse)
    elif tool.upper() == 'Pillow'.upper() :
        displayImageWithPillow(imgFile, labelsResponse)
    elif tool.upper() == 'OpenCV'.upper() :
        displayImageWithOpenCV(imgFile, labelsResponse)
    elif tool == "-" :
        print()
        print("No display option specified")
    else :
        print()
        print("Unknown display tool:", tool)

if __name__ == "__main__" :    
    main(sys.argv)

# https://towardsdatascience.com/image-manipulation-tools-for-python-6eb0908ed61f
# https://www.geeksforgeeks.org/working-images-python/