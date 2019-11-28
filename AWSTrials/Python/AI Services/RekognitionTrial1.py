# Based on Amazon's example https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html

import sys
import os

import boto3
import pprint

import pickle

def detect_labels_local_file(imgFile) :

    # Check for a cached response file
    cacheFolder = "AI Services/responsesCache"
    basename = os.path.basename(imgFile)

    cacheFile = cacheFolder + "/" + basename + ".response"
    prettyCacheFile = cacheFolder + "/" + basename + ".response.pretty.txt"

    if os.path.isfile(cacheFile) :
        print('Cache file ', cacheFile, ' found')

        with open(cacheFile, 'rb') as f:
            response = pickle.load(f)
            print('Read from cache file', cacheFile)
    else :
        print('No cache file ', cacheFile, ' found')

        client = boto3.client('rekognition')

        with open(imgFile, 'rb') as image :
            response = client.detect_labels(Image={'Bytes' : image.read() })
            print('*** Invoked Rekognition ***')

        with open(cacheFile, 'wb') as f:
            pickle.dump(response, f)
            print('Written to cache file', cacheFile)

    pp = pprint.PrettyPrinter(indent=4)
    pstring = pp.pformat(response)
    #print(pstring)
    with open(prettyCacheFile, 'w') as f:
        f.write(pstring)
        print('Written response to pretty file', prettyCacheFile)

    print()
    print('Labels reported in {0}:'.format(imgFile))
    print()
    for label in response['Labels'] :
        parents = ", ".join([ d['Name'] for d in label['Parents'] ])
        conf_s = "{0:.1f}%".format(label['Confidence'])
        instanceCount = len(label['Instances'])
        parentCount = len(label['Parents'])
        print("{0:20.20s} {1}   instances = {2:2d}   parents = {3}".format(label['Name'], conf_s, instanceCount, parents))
        # if parentCount > 0 :
        #     print(label['Name'] + " : " + conf_s + " : parents = " + parents)
        # else :
        #     print(label['Name'] + " : " + conf_s)
        # if instanceCount > 0 :
        #     print("- instances = ", instanceCount)

    return response

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
        conf_s = "{0:.1f}%".format(label['Confidence'])
        #if(len(instances) == 0) :
        #    print("{0} : {1}".format(label['Name'], conf_s))
        #else :
        #    print("{0} : {1} : {2} instance(s)".format(label['Name'], conf_s, len(instances)))
        if label['Name'] == "Person" :
            boxc = 'red'
        elif len(instances):
            boxc = 'green'

        for instance in instances :
            conf_s = "{0:.1f}%".format(instance['Confidence'])
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
    rowSetting = 6
    fig = plt.figure(figsize=(colSetting, rowSetting))
    grid = plt.GridSpec(4, len(items), hspace=1.2)
    
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

    horizontalSize, verticalSize = img.size   # (x,y) NB Opposite way round from matplotlib

    labels = labelsResponse['Labels']
    rects = []
    items = []
    for label in labels:
        instances = label['Instances']
        conf_s = "{0:.1f}%".format(label['Confidence'])
        # if(len(instances) == 0) :
        #     print("{0} : {1}".format(label['Name'], conf_s))
        # else :
        #     print("{0} : {1} : {2} instance(s)".format(label['Name'], conf_s, len(instances)))
        if label['Name'] == "Person" :
            boxc = 'red'
        elif len(instances):
            boxc = 'green'

        for instance in instances :
            conf_s = "{0:.1f}%".format(instance['Confidence'])
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
        conf_s = "{0:.1f}%".format(label['Confidence'])
        # if(len(instances) == 0) :
        #     print("{0} : {1}".format(label['Name'], conf_s))
        # else :
        #     print("{0} : {1} : {2} instance(s)".format(label['Name'], conf_s, len(instances)))
        if label['Name'] == "Person" :
            boxc = bgrcolorRed
        elif len(instances):
            boxc = bgrcolorGreen

        for instance in instances :
            conf_s = "{0:.1f}%".format(instance['Confidence'])
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
    if len(argv) == 1 :
        print("No image file argument provided")
        imgFile = 'AI Services/woodbridge.jpg'
        print("Using default image file location: ", imgFile)
    else :
        imgFile = argv[1]

    labelsResponse = detect_labels_local_file(imgFile)

    displayImageWithMatPlotLib(imgFile, labelsResponse)
    #displayImageWithPillow(imgFile, labelsResponse)
    #displayImageWithOpenCV(imgFile, labelsResponse)

if __name__ == "__main__" :    
    main(sys.argv)
