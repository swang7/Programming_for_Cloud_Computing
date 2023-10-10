# create user file
echo "create user file, /tmp/user_file.txt"
echo "This is a user file " > /tmp/user_file.txt
cat /tmp/user_file.txt
echo

# create another user file with space in name
echo "create test file, /tmp/test file.txt"
echo "This is a test file" > "/tmp/test file.txt"
cat "/tmp/test file.txt"
echo 

# Create user
# 1. wrong arguments, show usage
echo "python3 createuser.py"
python3 createuser.py
echo
# 2. right arguments
echo "python3 createuser.py amy a_pw amy@email.com"
python3 createuser.py amy a_pw amy@email.com
echo
# 3. update user password
echo "python3 createuser.py amy amy_pw amy@email.com"
python3 createuser.py amy amy_pw amy@email.com
echo
echo

# list user files
# 1. wrong arguments, show usage
echo "python3 listfiles.py"
python3 listfiles.py
echo
# 2. right arguments
echo "python3 listfiles.py amy amy_pw"
python3 listfiles.py amy amy_pw
echo
# 3. wrong password
echo "python3 listfiles.py amy a_pw"
python3 listfiles.py amy a_pw
echo
# 4. invalid user name
echo "python3 listfiles.py sam a_pw"
python3 listfiles.py sam a_pw
echo
echo

# upload file
# 1. wrong arguments, show usage
echo "python3 uploadfile.py"
python3 uploadfile.py
echo
# 2. upload user_file.txt
echo "python3 uploadfile.py amy amy_pw amy_file /tmp/user_file.txt"
python3 uploadfile.py amy amy_pw amy_file /tmp/user_file.txt
echo
# 2a. list file
echo "python3 listfiles.py amy amy_pw"
python3 listfiles.py amy amy_pw
echo
# 3. upload "test file.txt
echo 'python3 uploadfile.py amy amy_pw "amy test" "/tmp/test file.txt"'
python3 uploadfile.py amy amy_pw "amy test" "/tmp/test file.txt"
echo
# 3a, list file
echo "python3 listfiles.py amy amy_pw"
python3 listfiles.py amy amy_pw
echo
echo

# get file
# 1. wrong arguments, show usage
echo "python3 getfile.py"
python3 getfile.py
echo
# 2. get user_file.txt
echo "python3 getfile.py amy amy_pw amy_file /tmp/amy_file.txt"
python3 getfile.py amy amy_pw amy_file /tmp/amy_file.txt
echo
# 2a cat user_file.txt content
echo "cat /tmp/amy_file.txt"
cat /tmp/amy_file.txt
echo
# 3. get "test file.txt"
echo 'python3 getfile.py amy amy_pw "amy test" "/tmp/amy test.txt"'
python3 getfile.py amy amy_pw "amy test" "/tmp/amy test.txt"
echo
# 3a cat "test file.txt" content
echo 'cat "/tmp/amy test.txt"'
cat "/tmp/amy test.txt"
echo
echo

# delete file
# 1. wrong arguments, show usage
echo "python3  deletefile.py"
python3  deletefile.py
echo
# 2. list current files
echo "python3 listfiles.py amy amy_pw"
python3 listfiles.py amy amy_pw
echo
# 3. delete user_file.txt
echo "python3  deletefile.py amy amy_pw amy_file"
python3  deletefile.py amy amy_pw amy_file
echo
# 3a. list files
echo "python3 listfiles.py amy amy_pw"
python3 listfiles.py amy amy_pw
echo
# 4. delete "test file".txt
echo 'python3  deletefile.py amy amy_pw "amy test"'
python3  deletefile.py amy amy_pw "amy test"
echo
# 4a. ist files
echo "python3 listfiles.py amy amy_pw"
python3 listfiles.py amy amy_pw
echo
