#!/bin/bash

INSTANCE_TAG_VALUE="ucscx-homework-2-part-1"
EBS_TAG="Homework"
EBS_TAG_VALUE="2.1"

function get_instance_id() {
    result=$(aws ec2 describe-instances --filters "Name=tag-value,Values=$INSTANCE_TAG_VALUE")
    EC_instance_id=$(jq -r '.Reservations[0].Instances[0].InstanceId' <<< $result)
    echo "ec2 instance id is $EC_instance_id"
}

function get_ebs_vol_id() {
    result=$(aws ec2 describe-volumes --filters Name=tag:$EBS_TAG,Values=$EBS_TAG_VALUE)
    EBS_vol_id=$(jq -r '.Volumes[0].VolumeId' <<< $result)
    echo "volumeId is $EBS_vol_id"
}

function detach_ebs_vol() {
    result=$(aws ec2 detach-volume --volume-id $EBS_vol_id)
    if [[ ${?} -eq 0 ]]; then
        echo "detach ebs VolumeId $EBS_vol_id"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

function stop_ec2_instance() {
    result=$(aws ec2 stop-instances --instance-ids $EC_instance_id)
    if [[ ${?} -eq 0 ]]; then
        echo "stopped ec2 InstanceId $EC_instance_id"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

# terminate ec2 instance
function terminate_ec2_instance() {
    result=$(aws ec2 terminate-instances --instance-ids $EC_instance_id)
    if [[ ${?} -eq 0 ]]; then
        echo "terminate ec2 InstanceId $EC_instance_id"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi    
}

get_instance_id
get_ebs_vol_id
stop_ec2_instance 
detach_ebs_vol
terminate_ec2_instance