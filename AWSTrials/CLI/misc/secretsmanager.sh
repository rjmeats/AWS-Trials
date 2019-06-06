. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List secrets:"
echo

aws secretsmanager list-secrets

echo
echo "Create secret:"
echo

SECRET_NAME=cli-test-secret
SECRET='[{"username":"bob"},{"password":"abc123xyz456"}]'

aws secretsmanager create-secret --name ${SECRET_NAME}  --description "Test Secret" --secret-string "${SECRET}"

echo
echo "Describe secret:"
echo

aws secretsmanager describe-secret --secret-id "${SECRET_NAME}"

echo
echo "Get secret value:"
echo

aws secretsmanager get-secret-value --secret-id "${SECRET_NAME}"

echo
echo "Delete secret with default delay:"
echo

aws secretsmanager delete-secret --secret-id "${SECRET_NAME}"

echo
echo "Describe secret:"
echo

aws secretsmanager describe-secret --secret-id "${SECRET_NAME}"

echo
echo "Restore secret before deletion date:"
echo

aws secretsmanager restore-secret --secret-id "${SECRET_NAME}"

echo
echo "Describe secret:"
echo

aws secretsmanager describe-secret --secret-id "${SECRET_NAME}"

echo
echo "Delete secret immediately:"
echo

aws secretsmanager delete-secret --secret-id "${SECRET_NAME}" --force-delete-without-recovery

