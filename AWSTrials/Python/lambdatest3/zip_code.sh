rm -f test3.zip

# Add the package folder content, without a 'package' level

cd package
"/c/Program Files/7-Zip"/7z.exe a -tzip ../test3.zip . 

# Add in the main Python module, at the same level
cd ..

echo

ls -ltr test3.zip

sleep 2

"/c/Program Files/7-Zip"/7z.exe a -tzip test3.zip test3.py 

ls -ltr test3.zip

sleep 2

"/c/Program Files/7-Zip"/7z.exe l test3.zip 


