# Setting aws as a command alias, and allow it to work in bash shell scripts.
#
# This works for some cases, but not if the command line contains a quoted string containing a space 
# alias aws=aws.cmd	
#
# So instead, invoke Python more directly against the 'aws' file delivered with the AWS CLI installation.
# This has been renamed to aws.py for clarity.
alias aws='py "/c/Program Files (x86)/Microsoft Visual Studio/Shared/Python36_64/Scripts/aws.py"'
shopt -s expand_aliases


