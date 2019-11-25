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

    return len(response['Labels'])


responseData = {
    'LabelModelVersion': '2.0',
    'Labels': [   {   'Confidence': 99.82268524169922,
                      'Instances': [   {   'BoundingBox': {   'Height': 0.16909795999526978, 
                                                              'Left': 0.06820300221443176,   
                                                              'Top': 0.8277932405471802,     
                                                              'Width': 0.04272410646080971}, 
                                           'Confidence': 99.82268524169922},
                                       {   'BoundingBox': {   'Height': 0.15416546165943146, 
                                                              'Left': 0.5912736654281616,    
                                                              'Top': 0.8358995318412781,     
                                                              'Width': 0.03701213747262955}, 
                                           'Confidence': 99.63651275634766},
                                       {   'BoundingBox': {   'Height': 0.17881029844284058, 
                                                              'Left': 0.10368393361568451,   
                                                              'Top': 0.8112196922302246,     
                                                              'Width': 0.044059377163648605},
                                           'Confidence': 99.09613800048828},
                                       {   'BoundingBox': {   'Height': 0.12659697234630585, 
                                                              'Left': 0.7360311150550842,
                                                              'Top': 0.8513647317886353,
                                                              'Width': 0.036163080483675},
                                           'Confidence': 98.90628814697266},
                                       {   'BoundingBox': {   'Height': 0.07913586497306824,
                                                              'Left': 0.8010864853858948,
                                                              'Top': 0.8757282495498657,
                                                              'Width': 0.028375662863254547},
                                           'Confidence': 97.51142883300781},
                                       {   'BoundingBox': {   'Height': 0.08081457018852234,
                                                              'Left': 0.8349905610084534,
                                                              'Top': 0.8889844417572021,
                                                              'Width': 0.03675871714949608},
                                           'Confidence': 96.9069595336914},
                                       {   'BoundingBox': {   'Height': 0.07370787858963013,
                                                              'Left': 0.918094277381897,
                                                              'Top': 0.8520969152450562,
                                                              'Width': 0.01993575505912304},
                                           'Confidence': 94.63079071044922},
                                       {   'BoundingBox': {   'Height': 0.14174315333366394,
                                                              'Left': 0.681219220161438,
                                                              'Top': 0.830905020236969,
                                                              'Width': 0.036407221108675},
                                           'Confidence': 92.64032745361328},
                                       {   'BoundingBox': {   'Height': 0.1237691268324852,
                                                              'Left': 0.7115389704704285,
                                                              'Top': 0.8515939712524414,
                                                              'Width': 0.023557396605610847},
                                           'Confidence': 90.84557342529297},
                                       {   'BoundingBox': {   'Height': 0.07659190893173218,
                                                              'Left': 0.6737658977508545,
                                                              'Top': 0.8920505046844482,
                                                              'Width': 0.019833331927657127},
                                           'Confidence': 83.75321197509766},
                                       {   'BoundingBox': {   'Height': 0.02695612981915474,
                                                              'Left': 0.18015721440315247,
                                                              'Top': 0.8343353867530823,
                                                              'Width': 0.01885409466922283},
                                           'Confidence': 79.75335693359375},
                                       {   'BoundingBox': {   'Height': 0.08857892453670502,
                                                              'Left': 0.7786628007888794,
                                                              'Top': 0.8762859106063843,
                                                              'Width': 0.018496662378311157},
                                           'Confidence': 68.13536071777344},
                                       {   'BoundingBox': {   'Height': 0.056151870638132095,
                                                              'Left': 0.830237627029419,
                                                              'Top': 0.8539053201675415,
                                                              'Width': 0.01896805502474308},
                                           'Confidence': 63.03844451904297},
                                       {   'BoundingBox': {   'Height': 0.07315158098936081,
                                                              'Left': 0.8303483724594116,
                                                              'Top': 0.8853803873062134,
                                                              'Width': 0.02594663016498089},
                                           'Confidence': 57.99748611450195}],
                      'Name': 'Person',
                      'Parents': []},
                  {   'Confidence': 99.82268524169922,
                      'Instances': [],
                      'Name': 'Human',
                      'Parents': []},
                  {   'Confidence': 99.20208740234375,
                      'Instances': [],
                      'Name': 'Automobile',
                      'Parents': [   {'Name': 'Vehicle'},
                                     {'Name': 'Transportation'}]},
                  {   'Confidence': 99.20208740234375,
                      'Instances': [],
                      'Name': 'Vehicle',
                      'Parents': [{'Name': 'Transportation'}]},
                  {   'Confidence': 99.20208740234375,
                      'Instances': [   {   'BoundingBox': {   'Height': 0.12690119445323944,
                                                              'Left': 0.14527611434459686,
                                                              'Top': 0.8588009476661682,
                                                              'Width': 0.13638289272785187},
                                           'Confidence': 99.20208740234375},
                                       {   'BoundingBox': {   'Height': 0.08672965317964554,
                                                              'Left': 0.28176191449165344,
                                                              'Top': 0.8530611991882324,
                                                              'Width': 0.09053219109773636},
                                           'Confidence': 88.03359985351562},
                                       {   'BoundingBox': {   'Height': 0.07676022499799728,
                                                              'Left': 0.2392818033695221,
                                                              'Top': 0.8535906672477722,
                                                              'Width': 0.07199025899171829},
                                           'Confidence': 71.88793182373047}],
                      'Name': 'Car',
                      'Parents': [   {'Name': 'Vehicle'},
                                     {'Name': 'Transportation'}]},
                  {   'Confidence': 99.20208740234375,
                      'Instances': [],
                      'Name': 'Transportation',
                      'Parents': []},
                  {   'Confidence': 98.20384216308594,
                      'Instances': [],
                      'Name': 'Building',
                      'Parents': []},
                  {   'Confidence': 97.72187042236328,
                      'Instances': [],
                      'Name': 'Nature',
                      'Parents': []},
                  {   'Confidence': 97.72187042236328,
                      'Instances': [],
                      'Name': 'Outdoors',
                      'Parents': []},
                  {   'Confidence': 97.72187042236328,
                      'Instances': [],
                      'Name': 'Rural',
                      'Parents': [   {'Name': 'Nature'},
                                     {'Name': 'Countryside'},
                                     {'Name': 'Outdoors'}]},
                  {   'Confidence': 97.72187042236328,
                      'Instances': [],
                      'Name': 'Countryside',
                      'Parents': [{'Name': 'Nature'}, {'Name': 'Outdoors'}]},
                  {   'Confidence': 97.72187042236328,
                      'Instances': [],
                      'Name': 'Shelter',
                      'Parents': [   {'Name': 'Nature'},
                                     {'Name': 'Countryside'},
                                     {'Name': 'Building'},
                                     {'Name': 'Rural'},
                                     {'Name': 'Outdoors'}]},
                  {   'Confidence': 95.83272552490234,
                      'Instances': [],
                      'Name': 'Housing',
                      'Parents': [{'Name': 'Building'}]},
                  {   'Confidence': 79.22653198242188,
                      'Instances': [],
                      'Name': 'House',
                      'Parents': [{'Name': 'Building'}, {'Name': 'Housing'}]},
                  {   'Confidence': 66.64527130126953,
                      'Instances': [],
                      'Name': 'Architecture',
                      'Parents': [{'Name': 'Building'}]},
                  {   'Confidence': 63.31800842285156,
                      'Instances': [],
                      'Name': 'Urban',
                      'Parents': []},
                  {   'Confidence': 59.7952766418457,
                      'Instances': [],
                      'Name': 'Tower',
                      'Parents': [   {'Name': 'Architecture'},
                                     {'Name': 'Building'}]},
                  {   'Confidence': 59.7952766418457,
                      'Instances': [],
                      'Name': 'Steeple',
                      'Parents': [   {'Name': 'Tower'},
                                     {'Name': 'Architecture'},
                                     {'Name': 'Building'}]},
                  {   'Confidence': 59.7952766418457,
                      'Instances': [],
                      'Name': 'Spire',
                      'Parents': [   {'Name': 'Tower'},
                                     {'Name': 'Architecture'},
                                     {'Name': 'Building'}]},
                  {   'Confidence': 57.83088684082031,
                      'Instances': [],
                      'Name': 'Neighborhood',
                      'Parents': [{'Name': 'Urban'}, {'Name': 'Building'}]},
                  {   'Confidence': 56.22208786010742,
                      'Instances': [],
                      'Name': 'Hut',
                      'Parents': [   {'Name': 'Nature'},
                                     {'Name': 'Countryside'},
                                     {'Name': 'Building'},
                                     {'Name': 'Rural'},
                                     {'Name': 'Outdoors'}]},
                  {   'Confidence': 55.91592025756836,
                      'Instances': [],
                      'Name': 'Roof',
                      'Parents': []}],
    'ResponseMetadata': {   'HTTPHeaders': {   'connection': 'keep-alive',
                                               'content-length': '5099',
                                               'content-type': 'application/x-amz-json-1.1',
                                               'date': 'Mon, 25 Nov 2019 '
                                                       '15:40:16 GMT',
                                               'x-amzn-requestid': '6034c5dc-e82b-47fe-92cd-e9b336c306f0'},
                            'HTTPStatusCode': 200,
                            'RequestId': '6034c5dc-e82b-47fe-92cd-e9b336c306f0',
                            'RetryAttempts': 0}}



def displayImageWithMatPlotLib(imgFile) :

# https://www.geeksforgeeks.org/reading-images-in-python/

    import matplotlib.image as mpimg 
    import matplotlib.pyplot as plt 

    img = mpimg.imread(imgFile) 
    fig, ax = plt.subplots()
    plt.imshow(img)

    #Fetching imaging size info from plot. But realised can get from image object more directly
    #verticalSize = abs(ax.get_ybound()[1] - ax.get_ybound()[0])
    #horizontalSize = abs(ax.get_xbound()[1] - ax.get_xbound()[0])

    verticalSize, horizontalSize, dummy = img.shape

    labels = responseData['Labels']
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
            boxheight = box['Height'] * verticalSize
            boxwidth = box['Width'] * horizontalSize
            topoffset = box['Top'] *verticalSize
            leftoffset = box['Left'] * horizontalSize
            # Plot a box on the image at the appropriate point
            ax.add_patch(plt.Rectangle((leftoffset, topoffset), boxwidth, boxheight, edgecolor=boxc, alpha=0.5, lw=1,facecolor='none'))

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

def main() :
    imgFile = 'AI Services/woodbridge.jpg'

    displayImageWithMatPlotLib(imgFile)
    #displayImageWithPillow(imgFile)
    #displayImageWithOpenCV(imgFile)
    #label_count = detect_labels_local_file(imgFile)
    #print("Labels detected :", str(label_count))

if __name__ == "__main__" :
    main()
