import os

import pickle           # To save response data in a simple local cache
import pprint           # Dump Python data structure showing the response in a readable format

# The cached response will be in a cache folder, with the cached
# file name derived from the image file name = NB the current simple scheme doesn't work when different
# images have the same file name! Also, doesn't clear the cache ever, or put a time limit on entries,
# so not operationally robust.

class Cacher :

    # Use cache folder specified in environment, if present, otherwise a default.
    envVarName = 'RESPONSE_CACHE_LOCATION'

    def __init__(self, itemTypeName, itemID) :
        self.itemTypeName = itemTypeName
        self.itemID = itemID

    def findCachedResponse(self) :
        response = None
        cacheDefault = os.path.join(os.path.dirname(__file__), 'responsesCache/' + self.itemTypeName.lower())
        self.cacheLocation = os.environ.get(self.envVarName, cacheDefault)

        # We cache two files per image: a 'pickle' format data structure, and a human-readable form of the same data
        self.cacheFile = os.path.join(self.cacheLocation, self.itemID + '.response')
        self.prettyCacheFile = os.path.join(self.cacheLocation, self.itemID + '.response.pretty.txt')

        if os.path.isfile(self.cacheFile) :
            print('Cache file {0} found ..'.format(self. cacheFile))

            with open(self.cacheFile, 'rb') as f:
                response = pickle.load(f)
                print('.. read pre-existing {0} response from cache file'.format(self.itemTypeName))
        else :
            print('No cache file {0} found.'.format(self.cacheFile))

        return response

    def storeResponseInCache(self, response) :

        if not os.path.isdir(self.cacheLocation) :
            os.makedirs(self.cacheLocation)
            print('Created {0} cache location {1}'.format(self.itemTypeName, self.cacheLocation))

        # Use pickle to cache the response data.
        with open(self.cacheFile, 'wb') as f:
            pickle.dump(response, f)
            print('Written {0} response as binary object to cache file {1}'.format(self.itemTypeName, self.cacheFile))

        # Produce a human-readable version of the response data structure, and cache this too.
        pp = pprint.PrettyPrinter(indent=4)
        pstring = pp.pformat(response)
        with open(self.prettyCacheFile, 'w', encoding='utf-8') as f:
            f.write(pstring)
            print('Dumped formatted {0} response to file {1}'.format(self.itemTypeName, self.prettyCacheFile))

        return response
