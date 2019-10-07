. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe instances:"
echo

aws rds describe-db-instances

echo
echo "Describe snapshots:"
echo

aws rds describe-db-snapshots

echo
echo "Describe clusters:"
echo

aws rds describe-db-clusters
