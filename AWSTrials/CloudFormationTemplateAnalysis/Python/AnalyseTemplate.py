import sys
import os
import collections
import cfn_flip

# Recursive check through nested dictionaries defining attributes of a resource, to
# find references to other resources, parameters etc, and return these as a list

def getRefs(d) :

    refs = []
    for k,v in d.items() :
        if k == 'Ref' :
            refs.append(v)
        elif k == 'Fn::GetAtt':            
                ref = v[0] + '.' + v[1]
                #print(k, v, ref)
                refs.append(ref)
        else :
            if type(v) == type(d) :

                refs.extend(getRefs(v))

    return refs

def extractParameterInfo(name, dIn) :

    knownTypes = ['String', 'Number', 'CommaDelimitedList',
                'AWS::EC2::KeyPair::KeyName', 
                'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>']

    noValue = '-'
    dOut = {}
    dOut['Name'] = name
    dOut['Description'] = dIn.get('Description', noValue)
    dOut['Type'] = dIn.get('Type', noValue)
    dOut['Default'] = dIn.get('Default', noValue)
    dOut['FullNode'] = dIn

    if dOut['Type'] not in knownTypes :
        print('Unknown parameter type: ', dOut['Type'])
    return dOut

def extractMetadataInfo(name, dIn) :

    dOut = {}
    dOut['Name'] = name
    dOut['FullNode'] = dIn
    return dOut

def extractMappingsInfo(name, dIn) :

    dOut = {}
    dOut['Name'] = name
    dOut['Options'] = list(dIn.keys())
    # Pull out the fields referenced for the first of the keys, assume other keys produce the same set
    fieldsList = []
    for k in dIn.keys() :
        dFields = dIn[k]
        fieldsList = list(dFields.keys())
        break

    dOut['Fields'] = fieldsList
    dOut['FullNode'] = dIn

    return dOut

def extractConditionsInfo(name, dIn) :

    dOut = {}
    dOut['Name'] = name
    dOut['Condition'] = str(dIn)
    dOut['FullNode'] = dIn
    return dOut


# Dictionary mapping the names of all items under the top-level section to their template section
allItems = {}

def analyseConfiguration(data) :
    
    resourceTypeCounts = collections.Counter()
    referencesCounts = collections.Counter()

    # Split out top-level items into their own dictionaries (or strings for a couple of simple cases)
    templateFormatVersion = ''
    description = ''
    parameters = {}
    metadata = {}
    mappings = {}
    conditions = {}

    for k,v in data.items() :
        # Print main section names
        print(k, ":")
        print("")
        if k == 'AWSTemplateFormatVersion' :
            templateFormatVersion = v
            print("- ", templateFormatVersion)

        if k == 'Description' :
            description = v
            print("- ", description)

        if k == 'Parameters' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                parameter = extractParameterInfo(k2, v2)
                parameters[k2] = parameter
                print("- {0:20.20s} : {1:50.50s}  {2:100.100s}".format(parameter['Name'], parameter['Type'], parameter['Description']))

        if k == 'Metadata' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                md = extractMetadataInfo(k2, v2)
                metadata[k2] = md
                print("- {0:30.30s}".format(md['Name']))

        if k == 'Mappings' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                mapping = extractMappingsInfo(k2, v2)
                mappings[k2] = mapping
                print("- {0:20.20s} : {1:30.30s} => {2:s}".format(mapping['Name'], ' | '.join(mapping['Options']), ' + '.join(mapping['Fields'])))

        if k == 'Conditions' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                con = extractConditionsInfo(k2, v2)
                conditions[k2] = con
                print("- {0:30.30s} : {1:s}".format(con['Name'], con['Condition']))

        if k == 'Outputs' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                desc = ''
                if 'Description' in v2 :
                    desc = v2['Description']
                #print("- ", k2, desc, v2['Value'])

        if k == 'Resources' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                #print("- ", k2, v2['Type'])
                resourceTypeCounts[v2['Type']] += 1
                # And show references to other resources, parameters, etc
                refs = getRefs(v2)
                if len(refs) > 0 :
                    #print("  - has refs to ", refs)
                    for r in refs :
                        referencesCounts[r] += 1

        print("")
        print("===========================================================================================================")
        print("")

    print("Resource types:")
    print
    for c in resourceTypeCounts.keys() :
        print(c, " : ", resourceTypeCounts[c])

    print("")
    print("Resources referenced from other resources:")
    print
    for c in referencesCounts.keys() :
        pass
        #print(c, " : ", referencesCounts[c])

    print("")
    print("All top-level items:")
    print
    for k,v in allItems.items() :
        pass
        # print(k, v)

def main(filename) :

    if not os.path.isfile(filename) :
        print("***",  filename, "is not a file", file=sys.stderr)
        return

    print("Processing file: ", filename)

    with open(filename) as f:
        str = f.read()
        print("File ", filename, " is ", len(str), " characters long")

    (data,format) = cfn_flip.load(str)

    print("... format is ", format)

    analyseConfiguration(data)

if __name__ == "__main__" :

    if len(sys.argv) == 1 :
        print("No filename command line argument provided")
        exit()

    filename = sys.argv[1]
    main(filename)
