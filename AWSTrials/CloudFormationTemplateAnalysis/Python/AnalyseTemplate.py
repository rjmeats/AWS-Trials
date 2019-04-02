import sys
import os
import collections
import cfn_flip         # https://github.com/awslabs/aws-cfn-template-flip
import csv
import re

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html

# Recursive check through lists and dictionaries defining attributes of a resource, to
# find references to other resources, parameters etc, and return these as a list
# Three sorts of references to other resources (or parameters, etc):
# 
#   1) an element with a key of "Ref", with the value identifying the resource
#
#                "ShardCount": {
#                    "Ref": "SourceStreamSize"
#                }
#
#   2) A GetAtt function call, where the value of the resource reference is a combination of the
#   two elements in the array
#
#                "TargetKeyId": {
#                    "Fn::GetAtt": [
#                        "EncryptionKey",
#                        "Arn"
#                    ]
#                }
#
#   3) A Sub function call, with the string passed in contains ${variable} identifiers to be substituted in
#   eg for the region, or IDs of other resources. Sometimes, but not always, the full field is the variable. And
#   potentially there can be more than one item to be substituted.
#
#       AutoScalingGroupName: !Sub ${EFSAutoScalingGroup}
#       Value: !Sub ${AWS::StackName}-instance
#       DashboardName: !Sub ${AWS::StackName}-${AWS::Region}
#       Resource:
#            - !Sub arn:aws:autoscaling:${AWS::Region}:${AWS::AccountId}:autoScalingGroup:*:autoScalingGroupName/${EFSAutoScalingGroup}
#
#   In the above examples, we would want to pull out the following as resource references:
#
#   1) ShardCount refers to SourceStreamSize
#   2) TargetKeyId refers to EncryptionKey.Arn
#   3.1) AutoScalingGroupName refers to EFSAutoScalingGroup
#   3.2) Value refers to (e.g.) rjm-efs-stack-instance
#   3.3) DashboardName refers to (e.g.): rjm-efs-stack-eu-west-2

def getRefs(fullKey, key, node, level=0) :

    dump = False
    if dump :
        print("...", level, fullKey, " : ", type(node))

    refs = []

    if isinstance(node, dict) :
        for k,v in node.items() :
            thisfullKey = fullKey + "." + k
            refs.extend(getRefs(thisfullKey, k, v, level+1))
    elif type(node) == list :

        # Have we got a GetAtt function ? (See case 2 in comments above). If so, just combine
        # the two array elements to form the referenced item, don't process the array further
        if key == 'Fn::GetAtt' :
            if len(node) == 2 :
                ref = node[0] + '.' + node[1]
                adjustedFullKey = fullKey[0:-11]     # Remove the .Fn::GetAtt from the end of the key
                refs.append( (adjustedFullKey, ref) )
                if dump :
                    print("   ... found GetAtt ", ref, adjustedFullKey)
            else :
                print("*** GetAtt array not expected size", fullKey, node)
        elif key == 'Fn::Sub' :
            # Might mean more complex version of Sub function being used, where mapping of values occurs before substitution ?
            print("*** Sub function has unexpected array node", fullKey, node)
        else :
            itemIndex = 0
            for item in node:
                thisfullKey = fullKey + "[" + str(itemIndex) + "]"
                refs.extend(getRefs(thisfullKey, key, item, level))
                itemIndex += 1
    else :
        if dump :
            print("   ... fully expanded end for ", level, fullKey, " : ", node)
        
        # Have we got a Ref value ? (See case 1 in comments above)
        if key == 'Ref' :
            if fullKey.endswith(".Ref") :
                adjustedfullKey = fullKey[0:-4]     # Remove the .Ref from the end of the key
                refs.append( (adjustedfullKey, node) )
                if dump :
                    print("   ... found ref ", level, adjustedfullKey, " : ", node)
            else :
                print("*** array of Refs not handled perhaps ????", fullKey)
        # Have we got a Sub function ? (See case 3 in comments above)
        if key == 'Fn::Sub' :
            if fullKey.endswith("Fn::Sub") :
                adjustedfullKey = fullKey[0:-8]     # Remove the .Fn::Sub from the end of the key
                # Find the ${} entries within the string using a regular expression, and add them
                # all as references to other resources and similar
                paramRe = r"\${.+?}"
                matches = re.findall(paramRe, node)
                if dump :
                    print("   ... found Sub ", level, adjustedfullKey, " : ", matches, node)
                for parameter in matches :
                    if parameter.startswith("${") and parameter.endswith("}") :
                        ref = parameter[2:-1]
                        refs.append( (adjustedfullKey, ref) )
                    else :
                        print("*** Sub parameter not handled ????", fullKey, node, parameter)

                if len(matches) == 0 :
                    pass
                    # Can happen, no parameter specified in node string - perhaps due to manual editting to no longer need one, but
                    # Sub was retained for potential use of a parameter again in future.
                    #print("*** Sub not handled - 0 refs found ????", fullKey, node)

                # But if not, could have multiple ${..} entries, perhaps embedded in other text .... Probably need to look at using re
            else :
                print("*** array of Sub functions not handled perhaps ????", fullKey)

    return refs

def extractParameterInfo(name, dIn) :

    knownTypes = [
                'String', 'Number', 
                'CommaDelimitedList',
                'AWS::EC2::AvailabilityZone::Name',
                'AWS::EC2::KeyPair::KeyName', 
                'AWS::EC2::VPC::Id', 
                'AWS::EC2::Subnet::Id',
                'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>',
                ]

    noValue = '-'
    dOut = {}
    dOut['Name'] = name
    dOut['Description'] = dIn.get('Description', noValue)
    dOut['Type'] = dIn.get('Type', noValue)
    dOut['Default'] = dIn.get('Default', noValue)
    dOut['FullNode'] = dIn

    unknownType = False
    if dOut['Type'].startswith('List<') and dOut['Type'].endswith('>') :
        baseType = dOut['Type'].replace('List<', '').replace('>', '')
    else :
        baseType = dOut['Type']

    if baseType not in knownTypes :
        unknownType = True

    return dOut, unknownType


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
    dOut['ConditionNodeString'] = str(dIn)
    dOut['FullNode'] = dIn
    return dOut

def extractOutputsInfo(name, dIn) :

    noValue = '-'
    dOut = {}
    dOut['Name'] = name
    dOut['Description'] = dIn.get('Description', noValue)
    dOut['ValueNodeString'] = str(dIn['Value'])
    dOut['FullNode'] = dIn
    return dOut

def extractResourcesInfo(name, dIn) :

    knownTypes = [
            'AWS::EC2::VPC', 'AWS::EC2::Subnet', 'AWS::EC2::InternetGateway', 'AWS::EC2::VPCGatewayAttachment',
            'AWS::EC2::NatGateway', 'AWS::EC2::VPCEndpoint', 
            'AWS::EC2::RouteTable', 'AWS::EC2::Route', 'AWS::EC2::SubnetRouteTableAssociation',
            'AWS::EC2::EIP', 'AWS::EC2::EIPAssociation',
            'AWS::ECS::Cluster', 'AWS::EC2::Instance', 'AWS::ECS::Service',
            'AWS::ECS::TaskDefinition',

            'AWS::EC2::SecurityGroup', 'AWS::EC2::SecurityGroupIngress', 

            'AWS::S3::Bucket', 'AWS::S3::BucketPolicy',
            'AWS::CloudFront::CloudFrontOriginAccessIdentity', 'AWS::CloudFront::Distribution',

            'AWS::IAM::Role', 'AWS::IAM::InstanceProfile', 'AWS::IAM::ManagedPolicy', 'AWS::IAM::Policy', 

            'AWS::KMS::Key', 'AWS::KMS::Alias',

            'AWS::AutoScaling::AutoScalingGroup', 'AWS::AutoScaling::LaunchConfiguration', 'AWS::AutoScaling::ScalingPolicy',
            'AWS::AutoScaling::LifecycleHook',

            'AWS::CloudWatch::Alarm', 'AWS::CloudWatch::Dashboard',

            'AWS::Logs::LogGroup', 'AWS::Logs::LogStream',

            'AWS::Events::Rule',

            'AWS::CloudTrail::Trail', 

            'AWS::SNS::Topic', 'AWS::SNS::TopicPolicy', 'AWS::SNS::Subscription',
            'AWS::SQS::Queue', 'AWS::SQS::QueuePolicy',

            'AWS::SSM::Parameter', 'AWS::SSM::Association', 
            'AWS::SSM::MaintenanceWindow', 'AWS::SSM::MaintenanceWindowTarget', 'AWS::SSM::MaintenanceWindowTask', 
            'AWS::SSM::ResourceDataSync',

            'AWS::ElasticLoadBalancingV2::LoadBalancer', 'AWS::ElasticLoadBalancingV2::Listener', 'AWS::ElasticLoadBalancingV2::TargetGroup',
            'AWS::ElasticLoadBalancing::LoadBalancer',

            'AWS::ApplicationAutoScaling::ScalableTarget', 'AWS::ApplicationAutoScaling::ScalingPolicy',

            'AWS::DynamoDB::Table',

            'AWS::Cognito::UserPool', 'AWS::Cognito::UserPoolClient', 'AWS::Cognito::IdentityPool', 'AWS::Cognito::IdentityPoolRoleAttachment',
            'AWS::Cognito::UserPoolUser', 'AWS::Cognito::UserPoolGroup', 'AWS::Cognito::UserPoolUserToGroupAttachment',


            'AWS::KinesisFirehose::DeliveryStream', 'AWS::Kinesis::Stream', 'AWS::KinesisAnalytics::Application', 'AWS::KinesisAnalytics::ApplicationOutput',

            'AWS::Lambda::EventSourceMapping', 'AWS::Lambda::Function', 'AWS::Lambda::Permission',

            'AWS::CloudFormation::Stack',

            'AWS::IoT::TopicRule', 'AWS::IoT::Thing', 'AWS::IoT::Policy',

            'AWS::ApiGateway::RestApi', 'AWS::ApiGateway::Deployment', 'AWS::ApiGateway::Resource', 'AWS::ApiGateway::Method', 'AWS::ApiGateway::Stage',
            'AWS::ApiGateway::ApiKey',

            'AWS::Elasticsearch::Domain',

            'AWS::Redshift::Cluster', 'AWS::Redshift::ClusterParameterGroup', 'AWS::Redshift::ClusterSubnetGroup',

            'AWS::CodePipeline::Pipeline', 'AWS::CodeBuild::Project', 'AWS::CodeDeploy::Application', 

            'AWS::EFS::FileSystem', 'AWS::EFS::MountTarget', 

            'AWS::ElasticBeanstalk::Application', 'AWS::ElasticBeanstalk::ApplicationVersion', 'AWS::ElasticBeanstalk::ConfigurationTemplate', 
            'AWS::ElasticBeanstalk::Environment',

            'AWS::Glue::Database', 'AWS::Glue::Job', 'AWS::Glue::Trigger', 

            'AWS::SageMaker::Model', 'AWS::SageMaker::NotebookInstance',

            'AWS::EMR::Cluster', 'AWS::EMR::Step',

            'AWS::StepFunctions::StateMachine'
                ]


    noValue = '-'
    dOut = {}
    dOut['Name'] = name
    dOut['Type'] = dIn.get('Type', noValue)
    dOut['Condition'] = dIn.get('Condition', noValue)
    dOut['PropertiesNodeString'] = str(dIn.get('Properties', {}))

    dOut['CreationPolicy'] = str(dIn.get('CreationPolicy', {}))
    dOut['DeletionPolicy'] = dIn.get('DeletionPolicy', noValue)
    dOut['DependsOn'] = str(dIn.get('DependsOn', []))
    dOut['Metadata'] = str(dIn.get('Metadata', {}))
    dOut['UpdatePolicy'] = str(dIn.get('UpdatePolicy', {}))
    dOut['UpdateReplacePolicy'] = dIn.get('UpdateReplacePolicy', noValue)

    dOut['FullNode'] = dIn

    unknownType = False
    if dOut['Type'] not in knownTypes :
        if not dOut['Type'].startswith('Custom::') :
            unknownType = True
    return dOut, unknownType

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html
AWS_PseudoParameters = ['AWS::AccountId', 'AWS::NotificationARNs', 'AWS::Partition', 'AWS::Region', 'AWS::StackId', 'AWS::StackName', 'AWS::URLSuffix', 'AWS::NoValue']

def removeField(resourceName) :
    r = resourceName
    dotIndex = r.find('.')
    if dotIndex != -1 :
        r = resourceName[0:dotIndex]

    return r

def addItemType(itemName, itemType) :
    if itemName in allItems :
        currentType = allItems[itemName]
        if type(currentType) == list :
            currentType.append(itemType)
        else :
            allItems[itemName] = [currentType, itemType]
    else :
        allItems[itemName] = itemType

def getItemType(itemName) :
    baseItem = removeField(itemName)
    if baseItem in allItems :
        itemType = allItems[baseItem]
    elif baseItem in AWS_PseudoParameters :
        itemType = 'Pseudo-parameter'
    else :
        itemType = '?'
        print("*** Could not find item type for", itemName)
    return itemType

# In detailed Resource listing, option not to include role-related resources and links. Also apply
# to some other resource types that clutter up the basic application structure

def suppressRolesAndSimilar(resourceType, showRoles) :
    if resourceType in ['AWS::IAM::Role', 'AWS::KMS::Key', 'AWS::KMS::Alias'] and not showRoles:
        return True
    else :
        return False

# Dictionary mapping the names of all items under the top-level section to their template section
allItems = {}

def analyseConfiguration(data) :
    
    resourceTypeCounts = collections.Counter()
    referencesCounts = collections.Counter()

    # Split out top-level items into their own dictionaries (or strings for a couple of simple cases)
    templateFormatVersion = ''
    description = ''
    allItems.clear()
    parameters = {}
    metadata = {}
    mappings = {}
    conditions = {}
    resources = {}
    unknownParameterTypes = []
    unknownResourceTypes = []
    outputs = {}

    for k,v in data.items() :
        # Print main section names
        try :
            itemCount = len(v)
        except TypeError :
            itemCount = -1

        if itemCount >= 0 :
            print("{0:s} : {1:d} item{2:s}".format(k, itemCount, "s" if itemCount != 1 else ""))
        else :
            print(k)

        print("")
        if k == 'AWSTemplateFormatVersion' :
            templateFormatVersion = v
            print("- ", templateFormatVersion)

        if k == 'Description' :
            description = v
            print("- ", description)

        if k == 'Parameters' :
            for k2, v2 in v.items() :
                addItemType(k2, 'Parameter')
                #allItems[k2] = 'Parameter'
                parameter, unknownType = extractParameterInfo(k2, v2)
                parameters[k2] = parameter
                if unknownType:
                    if parameter['Type'] not in unknownParameterTypes :
                        unknownParameterTypes.append(parameter['Type'])
                print("- {0:20.20s} : {1:50.50s}  {2:.100s}".format(parameter['Name'], parameter['Type'], parameter['Description']))

        if k == 'Metadata' :
            for k2, v2 in v.items() :
                addItemType(k2, k)
                #allItems[k2] = k
                md = extractMetadataInfo(k2, v2)
                metadata[k2] = md
                print("- {0:30.30s}".format(md['Name']))

        if k == 'Mappings' :
            for k2, v2 in v.items() :
                addItemType(k2, 'Mapping')
                #allItems[k2] = 'Mapping'
                mapping = extractMappingsInfo(k2, v2)
                mappings[k2] = mapping
                print("- {0:20.20s} : {1:30.30s} => {2:s}".format(mapping['Name'], ' | '.join(mapping['Options']), ' + '.join(mapping['Fields'])))

        if k == 'Conditions' :
            for k2, v2 in v.items() :
                addItemType(k2, 'Condition')
                #allItems[k2] = 'Condition'
                con = extractConditionsInfo(k2, v2)
                conditions[k2] = con
                print("- {0:30.30s} : {1:s}".format(con['Name'], con['ConditionNodeString']))

        if k == 'Outputs' :
            for k2, v2 in v.items() :
                addItemType(k2, 'Output')
                #allItems[k2] = 'Output'
                output = extractOutputsInfo(k2, v2)
                outputs[k2] = output
                print("- {0:30.30s} : {1:40.40s} {2:s}".format(output['Name'], output['Description'], output['ValueNodeString']))

        if k == 'Resources' :
            for k2, v2 in v.items() :
                addItemType(k2, 'Resource')                
                #allItems[k2] = 'Resource'
                resource, unknownType = extractResourcesInfo(k2, v2)
                resources[k2] = resource
                if unknownType:
                    if resource['Type'] not in unknownResourceTypes :
                        unknownResourceTypes.append(resource['Type'])
                print("- {0:30.30s} : {1:50.50s} {2:60.60s}".format(resource['Name'], resource['Type'], resource['PropertiesNodeString']))
                resourceTypeCounts[resource['Type']] += 1
                # And show references to other resources, parameters, etc
                refs = getRefs(k2, k2, v2)
                resource['RefersTo'] = refs
                resource['ReferencedBy'] = []   # Filled in below
                if len(refs) > 0 :
                    for k,r in refs :

                        #print("  - has ref to ", k, " : ", r)
                        r = removeField(r)
                        referencesCounts[r] += 1

        print()
        print("===========================================================================================================")
        print()

    # Set up referenced-from info, for each item referenced from a resource
    for k,v in resources.items() :
        for field, item in v['RefersTo'] :
            itemType = getItemType(item)
            baseItem = removeField(item)
            if itemType == 'Resource' or 'Resource' in itemType:
                if baseItem in resources :
                    referencedResource = resources[baseItem]
                    referencedByInfo = (k, v['Type'], field)
                    referencedResource['ReferencedBy'].append(referencedByInfo)
                else :
                    print("*** Could not find referenced resource ", baseItem, " referenced from ", k)
            #print(k, field, item, baseItem, itemType)

    print()
    print("===========================================================================================================")
    print()

    itemCount = len(resources)
    print("{0:s} : {1:d} item{2:s}".format("Resources II", itemCount, "s" if itemCount != 1 else ""))
    print()
    if(not showRoles) :
        print("- omitting role and other similar resources")
        print()

    for k,v in resources.items() :
        if suppressRolesAndSimilar(v['Type'], showRoles) :
            continue

        print("- {0:s} ( {1:s} )".format(v['Name'], v['Type']))
        refs = v['RefersTo']
        for k2,ref in refs :
            refType = getItemType(ref)
            if type(refType) == list and 'Resource' in refType :
                # Resource name also used by e.g. an Output or a Condition
                refType = 'Resource'
            if refType not in ['Parameter', 'Pseudo-parameter'] :
                if refType == 'Resource' :
                    referredToResourceType = resources[removeField(ref)]['Type']
                    if suppressRolesAndSimilar(referredToResourceType, showRoles) :
                        continue
                adjustedField = k2[len(v['Name'])+1:]
                print("  - has ref to", refType, ref, "as", adjustedField)
        refsFrom = v['ReferencedBy']
        if len(refsFrom) > 0 :
            for (referrer, referrerType, referrerField) in refsFrom :
                adjustedField = referrerField[len(referrer)+1:]                    
                if suppressRolesAndSimilar(referrerType, showRoles) :
                    continue
                print("  - has ref from", referrer, "(", referrerType, ")", "as", adjustedField)

    print()
    print("===========================================================================================================")
    print()

    print("Resource types:")
    print()
    for c in resourceTypeCounts.keys() :
        print("- {0:50.50s} : {1:d}".format(c, resourceTypeCounts[c]))

    print()
    print("Resources referenced from other resources:")
    print()
    for c in referencesCounts.keys() :
        itemType = getItemType(c)
        if type(itemType) == list and 'Resource' in refType :
            # Resource name also used by e.g. an Output or a Condition
            itemType = 'Resource'
        print("- {0:50.50s} : {1:s} : {2:d}".format(c, str(itemType), referencesCounts[c]))

    print()
    print("All top-level items:")
    print()
    for k,v in allItems.items() :
        pass
        print("- {0:50.50s} : {1:30.30s}".format(k, str(v)))

    if len(unknownParameterTypes) > 0 :
        print("*** Unknown parameter type(s): ", unknownParameterTypes)

    if len(unknownResourceTypes) > 0 :
        print("*** Unknown resource type(s): ", unknownResourceTypes)

    results = {}
    results['Description'] = description
    results['Parameters'] = parameters
    results['Metadata'] = metadata
    results['Mappings'] = mappings
    results['Conditions'] = conditions
    results['Resources'] = resources
    results['ResourceTypeCounts'] = resourceTypeCounts
    results['Outputs'] = outputs
    results['AllItems'] = allItems
    return results

def generateResourceTypeCSV(contents, CSVFilename) :

    print("Writing resource types CSV output to file ", CSVFilename, " ...")
    with open(CSVFilename, "w", newline="") as csvfile:
        myCSVWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        myCSVWriter.writerow(["Template", "Resource Type", "Cases"])

        for template, content in contents.items() :
            counts = content['ResourceTypeCounts']
            for c in counts.keys() :
                tname = template if not template.endswith(".template") else template.replace(".template", "")
                myCSVWriter.writerow([ tname, c, counts[c] ])

def generateSectionsCSV(contents, CSVFilename) :

    print("Writing sections CSV output to file ", CSVFilename, " ...")
    with open(CSVFilename, "w", newline="") as csvfile:
        myCSVWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        myCSVWriter.writerow(["Template", "Section", "Cases"])

        for template, content in contents.items() :
            for section, sectionContents in content.items() :
                if type(sectionContents) == list or isinstance(sectionContents, dict) :
                    c = len(sectionContents)
                else :
                    c = 1

                if not section in ['ResourceTypeCounts', 'AllItems'] :
                    tname = template if not template.endswith(".template") else template.replace(".template", "")
                    myCSVWriter.writerow([ tname, section, c ])


def main(filenameArg, outDir="", showRoles=True) :

    filenames = []

    if os.path.isfile(filenameArg) :
        filenames.append(filenameArg)
    elif os.path.isdir(filenameArg):
        dirname = filenameArg
        for filename in os.listdir(dirname) :
            fullpath = dirname + "/" + filename
            if os.path.isdir(fullpath) :
                print("*** ignoring sub-directory ", filename)
            elif os.path.isfile(fullpath) :
                filenames.append(fullpath)
            else :
                print("*** ignoring non-file ", filename)
    else :
        print("***",  filename, "is not a file or directory", file=sys.stderr)
        return

    bulkRun = len(filenames) > 1
    if outDir == "" :
        outDir = "./output"

    if not os.path.isdir(outDir) :
        print("*** ", outDir, " is not a directory")
        outDir = ""
        return

    contents = {}
    for filename in filenames:
        baseTemplateName = os.path.basename(filename)
        with open(filename) as f:
            str = f.read()

        # Redirect output to file if not doing a bulk run
        print("Processing file ", filename, ", length", len(str), "characters ...")
        oldstdout = sys.stdout
        if bulkRun and 1 == 2:
            sys.stdout = None
        elif outDir != "" :
            outputFileName = outDir + "/" + baseTemplateName + ".txt"
            print("Output redirected to file ", outputFileName)
            sys.stdout = open(outputFileName, 'w')

        (data,format) = cfn_flip.load(str)
        #(data) = cfn_flip.load_yaml(str)
        #format = "yaml"
        print("{0:s}  ({1:s})".format(baseTemplateName, format))
        print()
        print()

        results = analyseConfiguration(data)
        sys.stdout = oldstdout
        # End of redirect

        contents[baseTemplateName] = results

    # Generate a csv file of template v resource type (+ count) listings
    #   xxx.template, resource, count        
    if bulkRun :
        if outDir != "" :
            CSVFilename = outDir + "/" + "resourceTypes.csv"
            generateResourceTypeCSV(contents, CSVFilename)
            CSVFilename = outDir + "/" + "sections.csv"
            generateSectionsCSV(contents, CSVFilename)
        else :
            print("No output CSV file specified for resource types")

if __name__ == "__main__" :

    if len(sys.argv) == 1 :
        print("*** No filename/dirname command line argument provided")
        exit()

    filename = sys.argv[1]
    outDir = sys.argv[2] if len(sys.argv) > 2 else ""
    showRolesArg = sys.argv[3] if len(sys.argv) > 3 else ""
    showRoles = not showRolesArg.lower() in ['roles=no', 'roles=n', 'roles=off', 'noroles', 'no-roles'] 

    main(filename, outDir, showRoles)


