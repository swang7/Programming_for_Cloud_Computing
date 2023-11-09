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
echo "bash createuser.sh"
bash createuser.sh
echo
# 2. right arguments
echo "bash createuser.sh amy a_pw amy@email.com"
bash createuser.sh amy a_pw amy@email.com
echo
# 3. update user password
echo "bash createuser.sh amy amy_pw amy@email.com"
bash createuser.sh amy amy_pw amy@email.com
echo
echo

# list user files
# 1. wrong arguments, show usage
echo "bash listfiles.sh"
bash listfiles.sh
echo
# 2. right arguments
echo "bash listfiles.sh amy amy_pw"
bash listfiles.sh amy amy_pw
echo
# 3. wrong password
echo "bash listfiles.sh amy a_pw"
bash listfiles.sh amy a_pw
echo
# 4. invalid user name
echo "bash listfiles.sh sam a_pw"
bash listfiles.sh sam a_pw
echo
echo

# upload file
# 1. wrong arguments, show usage
echo "bash uploadfile.sh"
bash uploadfile.sh
echo
# 2. upload user_file.txt
echo "bash uploadfile.sh amy amy_pw amy_file /tmp/user_file.txt"
bash uploadfile.sh amy amy_pw amy_file /tmp/user_file.txt
echo
# 2a. list file
echo "bash listfiles.sh amy amy_pw"
bash listfiles.sh amy amy_pw
echo
# 3. upload "test file.txt
echo 'bash uploadfile.sh amy amy_pw "amy test" "/tmp/test file.txt"'
bash uploadfile.sh amy amy_pw "amy test" "/tmp/test file.txt"
echo
# 3a, list file
echo "bash listfiles.sh amy amy_pw"
bash listfiles.sh amy amy_pw
echo
echo

# get file
# 1. wrong arguments, show usage
echo "bash getfile.sh"
bash getfile.sh
echo
# 2. get user_file.txt
echo "bash getfile.sh amy amy_pw amy_file /tmp/amy_file.txt"
bash getfile.sh amy amy_pw amy_file /tmp/amy_file.txt
echo
# 2a cat user_file.txt content
echo "cat /tmp/amy_file.txt"
cat /tmp/amy_file.txt
echo
# 3. get "test file.txt"
echo 'bash getfile.sh amy amy_pw "amy test" "/tmp/amy test.txt"'
bash getfile.sh amy amy_pw "amy test" "/tmp/amy test.txt"
echo
# 3a cat "test file.txt" content
echo 'cat "/tmp/amy test.txt"'
cat "/tmp/amy test.txt"
echo
echo

# delete file
# 1. wrong arguments, show usage
echo "bash  deletefile.sh"
bash  deletefile.sh
echo
# 2. list current files
echo "bash listfiles.sh amy amy_pw"
bash listfiles.sh amy amy_pw
echo
# 3. delete user_file.txt
echo "bash  deletefile.sh amy amy_pw amy_file"
bash  deletefile.sh amy amy_pw amy_file
echo
# 3a. list files
echo "bash listfiles.sh amy amy_pw"
bash listfiles.sh amy amy_pw
echo
# 4. delete "test file".txt
echo 'bash  deletefile.sh amy amy_pw "amy test"'
bash  deletefile.sh amy amy_pw "amy test"
echo
# 4a. ist files
echo "bash listfiles.sh amy amy_pw"
bash listfiles.sh amy amy_pw
echo
