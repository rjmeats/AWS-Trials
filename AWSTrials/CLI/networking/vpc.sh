. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "VPCs:"
echo

aws ec2 describe-vpcs

echo
echo "Subnets:"
echo

aws ec2 describe-subnets

echo
echo "Routing tables:"
echo

aws ec2 describe-route-tables

echo
echo "Network interfaces:"
echo

aws ec2 describe-network-interfaces

echo
echo "Security groups:"
echo

aws ec2 describe-security-groups


echo
echo "Network ACLs:"
echo

aws ec2 describe-network-acls

echo
echo "Internet Gateways:"
echo

aws ec2 describe-internet-gateways


echo
echo "NAT Gateways:"
echo

aws ec2 describe-nat-gateways


echo
echo "VPN Gateways:"
echo

aws ec2 describe-vpn-gateways

echo
echo "Customer Gateways:"
echo

aws ec2 describe-customer-gateways

echo
echo "Peering connections:"
echo

aws ec2 describe-vpc-peering-connections





