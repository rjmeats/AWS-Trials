import sys
import os
import collections
import cfn_flip         # https://github.com/awslabs/aws-cfn-template-flip

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html

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
                'List<AWS::EC2::AvailabilityZone::Name>',
                'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>']

    noValue = '-'
    dOut = {}
    dOut['Name'] = name
    dOut['Description'] = dIn.get('Description', noValue)
    dOut['Type'] = dIn.get('Type', noValue)
    dOut['Default'] = dIn.get('Default', noValue)
    dOut['FullNode'] = dIn

    if dOut['Type'] not in knownTypes :
        print('Unknown parameter type: [', dOut['Type'], ']')
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
            'AWS::ECS::Cluster', 'AWS::EC2::Instance',
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

            'AWS::SNS::Topic',
            'AWS::SQS::Queue', 'AWS::SQS::QueuePolicy',

            'AWS::SSM::Parameter', 'AWS::SSM::Association', 
            'AWS::SSM::MaintenanceWindow', 'AWS::SSM::MaintenanceWindowTarget', 'AWS::SSM::MaintenanceWindowTask', 
            'AWS::SSM::ResourceDataSync',

            'AWS::ElasticLoadBalancingV2::LoadBalancer', 'AWS::ElasticLoadBalancingV2::Listener', 'AWS::ElasticLoadBalancingV2::TargetGroup',
            'AWS::ElasticLoadBalancing::LoadBalancer',

            'AWS::ApplicationAutoScaling::ScalableTarget', 'AWS::ApplicationAutoScaling::ScalingPolicy',

            'AWS::DynamoDB::Table',

            'AWS::Cognito::UserPool', 'AWS::Cognito::UserPoolClient', 'AWS::Cognito::IdentityPool', 'AWS::Cognito::IdentityPoolRoleAttachment',
            'AWS::Cognito::UserPoolUser',

            'AWS::KinesisFirehose::DeliveryStream', 'AWS::Kinesis::Stream', 'AWS::KinesisAnalytics::Application', 'AWS::KinesisAnalytics::ApplicationOutput',

            'AWS::Lambda::EventSourceMapping', 'AWS::Lambda::Function', 'AWS::Lambda::Permission',

            'AWS::CloudFormation::Stack',

            'AWS::IoT::TopicRule', 'AWS::IoT::Thing', 'AWS::IoT::Policy',

            'AWS::ApiGateway::RestApi', 'AWS::ApiGateway::Deployment', 'AWS::ApiGateway::Resource', 'AWS::ApiGateway::Method', 'AWS::ApiGateway::Stage',
            'AWS::ApiGateway::ApiKey'

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

    unknownType = False

    noValue = '-'
    dOut = {}
    dOut['Name'] = name
    dOut['Type'] = dIn.get('Type', noValue)
    dOut['PropertiesNodeString'] = str(dIn.get('Properties', {}))

    dOut['CreationPolicy'] = str(dIn.get('CreationPolicy', {}))
    dOut['DeletionPolicy'] = dIn.get('DeletionPolicy', noValue)
    dOut['DependsOn'] = str(dIn.get('DependsOn', []))
    dOut['Metadata'] = str(dIn.get('Metadata', {}))
    dOut['UpdatePolicy'] = str(dIn.get('UpdatePolicy', {}))
    dOut['UpdateReplacePolicy'] = dIn.get('UpdateReplacePolicy', noValue)

    dOut['FullNode'] = dIn

    if dOut['Type'] not in knownTypes :
        if not dOut['Type'].startswith('Custom::') :
            print('Unknown resource type: ', dOut['Type'])
            unknownType = True
    return dOut, unknownType


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
    resources = {}
    unknownResourceTypes = []
    outputs = {}

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
                print("- {0:30.30s} : {1:s}".format(con['Name'], con['ConditionNodeString']))

        if k == 'Outputs' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                output = extractOutputsInfo(k2, v2)
                outputs[k2] = output
                print("- {0:30.30s} : {1:40.40s} {2:s}".format(output['Name'], output['Description'], output['ValueNodeString']))

        if k == 'Resources' :
            for k2, v2 in v.items() :
                allItems[k2] = k
                resource, unknownType = extractResourcesInfo(k2, v2)
                resources[k2] = resource
                if unknownType:
                    if resource['Type'] not in unknownResourceTypes :
                        unknownResourceTypes.append(resource['Type'])
                print("- {0:30.30s} : {1:50.50s} {2:60.60s}".format(resource['Name'], resource['Type'], resource['PropertiesNodeString']))
                resourceTypeCounts[resource['Type']] += 1
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

    if len(unknownResourceTypes) > 0 :
        print()
        print("Unknown resource types: ", unknownResourceTypes)

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
