#cloud-config
hostname: "aws_hw4_instance"
runcmd:
- sudo mkfs -t xfs /dev/xvdf
- sudo mkdir /mnt/hw4 -p
- sudo echo '/dev/xvdf /mnt/hw4 xfs defaults 0 0' >> /etc/fstab
- sudo mount -a
- echo 'Hello, world' >  /mnt/hw4/hello.txt
output : { all : '| tee -a /var/log/cloud-init-output.log' }