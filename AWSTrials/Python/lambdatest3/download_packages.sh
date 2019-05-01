if [[ -d package ]]
then
	echo "Deleting existing package folder"
	rm -r package
fi

mkdir package

cd package

pip install bs4 --target .

echo
echo
cd ..
ls -ltr package

