# Session-based boto3 commands to list options

import boto3

s = boto3.Session()

print()
print("Available services:")
print()
print(s.get_available_services())

print()
print("Available resources:")
print()
print(s.get_available_resources())

print()
print("Available regions for S3:")
print()
print(s.get_available_regions('s3'))

print()
print("Available partitions:")
print()
print(s.get_available_partitions())

print()
print("Credentials:")
print()
cred = s.get_credentials()
print("Access key:", cred.access_key)
print("Secret key:", cred.secret_key)
print("Token:", cred.token)
print("Method:", cred.method)

print()
print("Available profiles:")
print()
print(s.available_profiles)

print()
print("Account / User:")
print()
id = boto3.client('sts').get_caller_identity().get('Account')
#alias = boto3.client('iam').list_account_aliases()['AccountAliases'][0]
user = boto3.client('iam').get_user()
print(id, user['User']['UserName'])
acc_summary = boto3.client('iam').get_account_summary()
print()
print(acc_summary)

print()
print('List users')
print()
users_list = boto3.client('iam').list_users()
print(users_list)

print()
print("Profile and region:")
print()
print(s.profile_name, s.region_name)
