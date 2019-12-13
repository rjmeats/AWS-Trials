import sys
import os

import boto3

import Cacher

# Trial French text from Le Monde article 
# https://www.lemonde.fr/international/article/2019/12/10/boris-johnson-parodie-une-scene-du-film-love-actually-et-agace-hugh-grant_6022351_3210.html
french = [
'''Le premier ministre britannique Boris Johnson a parodié une scène du film Love actually, mardi 10 décembre, 
à deux jours des élections législatives, s’attirant des critiques cinglantes de Hugh Grant, star de cette comédie 
romantique et farouche opposant du Brexit.
''',
'''Dans la vidéo postée sur Twitter, on voit Boris Johnson sonner à la porte d’une électrice, promettant, 
à l’aide de pancartes, qu’« avec un peu de chance, d’ici l’année prochaine, on aura réalisé le Brexit (si le Parlement 
ne le bloque pas de nouveau) ».
''',
'''
Le premier ministre lui enjoint de voter pour son parti et de lui donner une confortable majorité au Parlement 
afin de « réaliser le Brexit », son slogan de campagne.
''',
'''
Il parodie ainsi une scène de la comédie romantique sortie en 2003 et réalisée par Richard Curtis, dans laquelle 
l’acteur Andrew Lincoln faisait passer un message silencieusement, à l’aide de pancartes, à une femme dont il était 
amoureux.
''',
'''
« J’ai trouvé que c’était plutôt bien fait (…) mais il est clair que le Parti conservateur a énormément d’argent.
C’est peut-être là que vont les roubles », a réagi Hugh Grant, en allusion aux accusations de financement russe 
du Parti conservateur.
'''
]

def translate(textFile, fromLanguage='en', toLanguage='fr') :
    # Check for a cached response file, using the image file name as the cache key. NB Will need
    # something more sophisticated to allow different images in files of the same base name to be used.
    textFileBasename = os.path.basename(textFile)
    with open(textFile, 'r', encoding='utf-8') as f :
        text = f.read()

    # Create a hash of the text to distinguish files with the same name but containing different text.
    # Only use a few digits of it to keep filename short.
    import hashlib
    textHashDigest = hashlib.sha256(text.encode()).hexdigest()
    cacheID = "{0}.{1}.{2}.{3}".format(textFileBasename, fromLanguage, toLanguage, textHashDigest[0:4])
    cacher = Cacher.Cacher('Translate', cacheID)
    cachedResponse = cacher.findCachedResponse()
    if cachedResponse == None :
        print('Invoking Translate ...')
        client = boto3.client('translate')
        # Boto3 converts the raw Rekognition HTTP response to a Python data structure. 
        response = client.translate_text(Text=text, SourceLanguageCode=fromLanguage, TargetLanguageCode=toLanguage)
        print('... response received from Translate')
        cacher.storeResponseInCache(response)
    else :
        response = cachedResponse

    return text, response

# #####################################################################################################

def main(argv) :

    if len(argv) > 1 and argv[1] != '-' :
        textFile = argv[1]
    else :
        textFile = 'AI Services/language.txt'
        print('No text file argument provided, using default : ', textFile)

    if len(argv) > 3 :
        sourceLang = argv[2]
        targetLang = argv[3]
    else :
        sourceLang = 'en'
        targetLang = 'fr'

    if not os.path.isfile(textFile) :
        print()
        print('*** File {0} not found'.format(textFile))
        return

    text, response = translate(textFile, fromLanguage=sourceLang, toLanguage=targetLang)

    bar = "=================================================================================="
    print('Converted:')
    print()
    print(bar)
    print(text)    
    print(bar)
    print()
    print('to:')
    print()
    print(bar)
    print(response['TranslatedText'])    
    print(bar)

if __name__ == '__main__' :    
    main(sys.argv)