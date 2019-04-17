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
print(s.get_credentials())

print()
print("Available profiles:")
print()
print(s.available_profiles)

print()
print("Profile and region:")
print()
print(s.profile_name, s.region_name)
