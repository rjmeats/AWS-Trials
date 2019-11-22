# Based on Amazon's example https://docs.aws.amazon.com/rekognition/latest/dg/images-bytes.html
import boto3

def detect_labels_local_file(imgFile) :
    client = boto3.client('rekognition')

    with open(imgFile, 'rb') as image :
        response = client.detect_labels(Image={'Bytes' : image.read() })

    print(response)
    print()
    print('Detected labels in ' + imgFile)
    for label in response['Labels'] :
        print(label['Name'] + " : " + str(label['Confidence']) + " : instances = " + str(len(label['Instances'])))

    return len(response['Labels'])

def main() :
    imgFile = 'AI Services/woodbridge.jpg'

    label_count = detect_labels_local_file(imgFile)
    print("Labels detected :", str(label_count))

if __name__ == "__main__" :
    main()