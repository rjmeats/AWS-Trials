if [[ -d package ]]
then
	echo "Deleting existing package folder"
	rm -r package
fi

mkdir package

cd package

pip install bs4 --target .
pip install requests --target .

echo
echo
cd ..
ls -ltr package

