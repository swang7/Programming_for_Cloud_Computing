#cloud-config
hostname: "az_hw7_instance"
runcmd:
- sudo mkfs -t xfs /dev/sdc
- sudo mkdir /mnt/hw7 -p
- sudo echo '/dev/sdc /mnt/hw7 xfs defaults 0 0' >> /etc/fstab
- sudo mount -a
- echo 'Hello, world' >  /mnt/hw7/hello.txt
output : { all : '| tee -a /var/log/cloud-init-output.log' }