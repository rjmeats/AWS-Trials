# Session-based boto3 commands to list options

import boto3

s = boto3.Session()

print("Available services:")
print()
print(s.get_available_services())
