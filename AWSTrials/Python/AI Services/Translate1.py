import boto3

translate = boto3.client('translate')

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

import pprint

for text in french[0:1] :
    result = translate.translate_text(Text=text, 
                SourceLanguageCode="fr", TargetLanguageCode="en")
    print('TranslatedText: ' + result.get('TranslatedText'))
    print()
    pp = pprint.PrettyPrinter(indent=4)
    pstring = pp.pformat(result)
    print(pstring)

print()
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))