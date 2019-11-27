# Based on Amazon's example https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html
import boto3
import pprint


def detect_labels_local_file(imgFile) :
    client = boto3.client('rekognition')

    with open(imgFile, 'rb') as image :
        response = client.detect_labels(Image={'Bytes' : image.read() })

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)

    print()
    print('Detected labels in ' + imgFile)
    for label in response['Labels'] :
        print(label['Name'] + " : " + str(label['Confidence']) + " : instances = " + str(len(label['Instances'])))

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

    #labels = responseData['Labels']
    patches = []
    labels = labelsResponse['Labels']
    items = []
    for label in labels:
        instances = label['Instances']
        if(len(instances) == 0) :
            print("{0} : {1:.1f}%".format(label['Name'], label['Confidence']))
        else :
            print("{0} : {1:.1f}% : {2} instance(s)".format(label['Name'], label['Confidence'], len(instances)))
#            print("{0} : {1} specific instance(s), confidence = {2:.1f}%".format(label['Name'], len(instances), label['Confidence']))
        if label['Name'] == "Person" :
            boxc = 'red'
        elif len(instances):
            boxc = 'green'

        for instance in instances :
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
            print(rectImg.shape)
            if len(items) < 20 :
                items.append((rectImg, label['Name']))
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
        sub_ax.set_title(items[i-1][1])
        sub_ax.set_yticklabels([])
        sub_ax.set_xticklabels([])
    plt.show()

def displayImageWithPillow(imgFile, labelsResponse) :

# https://www.geeksforgeeks.org/reading-images-in-python/
# https://pillow.readthedocs.io/en/stable/

    from PIL import Image, ImageDraw, ImageColor

    img = Image.open(imgFile) 

    horizontalSize, verticalSize = img.size   # (x,y) NB Opposite way round from matplotlib

    labels = labelsResponse['Labels']
    rects = []
    items = []
    for label in labels:
        instances = label['Instances']
        conf_s = "{0:.1f}%".format(label['Confidence'])
        if(len(instances) == 0) :
            print("{0} : {1}".format(label['Name'], conf_s))
        else :
            print("{0} : {1} : {2} instance(s)".format(label['Name'], conf_s, len(instances)))
        if label['Name'] == "Person" :
            boxc = 'red'
        elif len(instances):
            boxc = 'green'

        for instance in instances :
            box = instance['BoundingBox']
            boxheight = int(box['Height'] * verticalSize)
            boxwidth = int(box['Width'] * horizontalSize)
            topoffset = int(box['Top'] *verticalSize)
            leftoffset = int(box['Left'] * horizontalSize)

            rect = leftoffset,topoffset, leftoffset+boxwidth, topoffset+boxheight
            rects.append((rect, boxc))

            crop = img.crop(rect)
            draw = ImageDraw.Draw(crop, mode='RGBA')
            draw.text((0,0), label['Name'] + "(" + conf_s + ")")

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
        if(len(instances) == 0) :
            print("{0} : {1}".format(label['Name'], conf_s))
        else :
            print("{0} : {1} : {2} instance(s)".format(label['Name'], conf_s, len(instances)))
        if label['Name'] == "Person" :
            boxc = bgrcolorRed
        elif len(instances):
            boxc = bgrcolorGreen

        for instance in instances :
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

            # if len(items) < 20 :
            #     items.append((rectImg, label['Name']))
            # else :
            #     print("Too many items to display - ignoring", label['Name'])


    for rect in rects :
        cv2.rectangle(img, rect[0], rect[1], thickness=1)

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


import sys, getopt

def main(argv) :
    if len(argv) == 1 :
        print("No image file argument provided")
        imgFile = 'AI Services/woodbridge.jpg'
        print("Using default image file location: ", imgFile, " with cached response data")
        import WoodbridgeResponse
        labelsResponse = WoodbridgeResponse.labelsResponse
    else :
        imgFile = argv[1]
        labelsResponse = detect_labels_local_file(imgFile)

    #imgFile = 'AI Services/burgos.jpg'

    #displayImageWithMatPlotLib(imgFile, labelsResponse)
    #displayImageWithPillow(imgFile, labelsResponse)
    displayImageWithOpenCV(imgFile, labelsResponse)
    #print("Labels detected :", str(label_count))

if __name__ == "__main__" :    
    main(sys.argv)
