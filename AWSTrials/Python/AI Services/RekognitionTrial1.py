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
            # Plot a box on the image at the appropriate point
            #ax.add_patch(plt.Rectangle((leftoffset, topoffset), boxwidth, boxheight, edgecolor=boxc, alpha=0.5, lw=1,facecolor='none'))
            patches.append(plt.Rectangle((leftoffset, topoffset), boxwidth, boxheight, edgecolor=boxc, alpha=0.5, lw=1,facecolor='none'))

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

def displayImageWithPillow(imgFile) :

# https://www.geeksforgeeks.org/reading-images-in-python/

    from PIL import Image

    img = Image.open(imgFile) 
    img.show() 
    print(img.format)     
    print(img.mode) 


def displayImageWithOpenCV(imgFile) :
    import cv2
    img = cv2.imread(imgFile)
    cv2.imshow('image', img)
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

    displayImageWithMatPlotLib(imgFile, labelsResponse)
    #displayImageWithPillow(imgFile)
    #displayImageWithOpenCV(imgFile)
    #print("Labels detected :", str(label_count))

if __name__ == "__main__" :    
    main(sys.argv)
