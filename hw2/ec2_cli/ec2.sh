#!/bin/bash

KEY_PAIR="aws-hw-keypair"
MY_IP="73.93.72.74/32"
SSH_SECURITY_GROUP="SSH-ONLY"
UBUNTU_IMAGE="ami-03f65b8614a860c29"
INSTANCE_TAG="Name"
INSTANCE_TAG_VALUE="ucscx-homework-2-part-1"
EBS_TAG="Homework"
EBS_TAG_VALUE="2.1"

# create security group for ssh permission
function create_security_group_ssh() {
    aws ec2 create-security-group --group-name "SSH-ONLY" --description "Only allow ssh"
    if [[ ${?} -eq 0 ]]; then
        echo "created security group $SSH_SECURITY_GROUP"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi
}

# allow ssh from my laptop, $MY_IP
function add_ssh_rule() {
    aws ec2 authorize-security-group-ingress \
        --group-name $SSH_SECURITY_GROUP \
        --protocol tcp \
        --port 22 \
        --cidr $MY_IP
    if [[ ${?} -eq 0 ]]; then
        echo "added ssh rule to $SSH_SECURITY_GROUP"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

# create EBS volume
function create_ebs_vol() {
    result=$(aws ec2 create-volume \
        --volume-type "standard" \
        --size 1 \
        --availability-zone us-west-2a \
        --tag-specifications "ResourceType=volume,Tags=[{Key=$EBS_TAG,Value=$EBS_TAG_VALUE}]")
    if [[ ${?} -eq 0 ]]; then
        EBS_vol_id=$(jq -r '.VolumeId' <<< $result)
        echo "created ebs, VolumeId $EBS_vol_id"
        aws ec2 wait volume-available --volume-ids $EBS_vol_id
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

# create & start EC2 instance with security group
function new_ec2_instance() {
    result=$(aws ec2 run-instances \
        --image-id $UBUNTU_IMAGE \
        --instance-type t2.micro \
        --placement AvailabilityZone=us-west-2a \
        --key-name "$KEY_PAIR" \
        --security-groups "SSH-ONLY" \
        --tag-specifications "ResourceType=instance,Tags=[{Key=$INSTANCE_TAG,Value=$INSTANCE_TAG_VALUE}]")
    if [[ ${?} -eq 0 ]]; then
        EC_instance_id=$(jq -r '.Instances[0].InstanceId' <<< $result)
        echo "new ec2, InstanceId $EC_instance_id"
        aws ec2 wait instance-running --instance-ids $EC_instance_id
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

function attach_volume() {
    # attach EBS to instance
    result=$(aws ec2 attach-volume --volume-id "$EBS_vol_id" \
        --instance-id "$EC_instance_id" --device "/dev/xvdf")
    if [[ ${?} -eq 0 ]]; then
        echo "attached ebs $EBS_vol_id to instance $EC_instance_id"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

create_security_group_ssh
add_ssh_rule
new_ec2_instance
create_ebs_vol
attach_volume
