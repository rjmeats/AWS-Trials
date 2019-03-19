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

    resourceTypeCounts = collections.Counter()

    for k,v in data.items() :
        # Print main section names
        print(k, ":")
        print("")
        if k in ['AWSTemplateFormatVersion', 'Description'] :
                print("- ", v)

        if k == 'Metadata' :
            for k2, v2 in v.items() :
                print("- ", k2)
                for k3, v3 in v2.items() :
                    print("  - ", k3)

        if k == 'Mappings' :
            for k2, v2 in v.items() :
                print("- ", k2)
                for k3, v3 in v2.items() :
                    print("  - ", k3)

        if k == 'Conditions' :
            for k2, v2 in v.items() :
                print("- ", k2)

        if k == 'Outputs' :
            for k2, v2 in v.items() :
                desc = ''
                if 'Description' in v2 :
                    desc = v2['Description']
                print("- ", k2, desc, v2['Value'])

        if k == 'Parameters' :
            for k2, v2 in v.items() :
                desc = ''
                if 'Description' in v2 :
                    desc = v2['Description']
                print("- ", k2, v2['Type'], desc)

        if k == 'Resources' :
            for k2, v2 in v.items() :
                print("- ", k2, v2['Type'])
                resourceTypeCounts[v2['Type']] += 1
                # And show references to other resources, parameters, etc
                refs = getRefs(v2)
                if len(refs) > 0 :
                    print("  - has refs to ", refs)

        print("")
        print("===========================================================================================================")
        print("")

    for c in resourceTypeCounts.keys() :
        print(c, " : ", resourceTypeCounts[c])

if __name__ == "__main__" :

    if len(sys.argv) == 1 :
        print("No filename command line argument provided")
        exit()

    filename = sys.argv[1]
    main(filename)
