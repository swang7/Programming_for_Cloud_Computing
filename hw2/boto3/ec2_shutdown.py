import boto3
from botocore.exceptions import ClientError

INSTANCE_TAG="Name"
INSTANCE_TAG_VALUE="ucscx-homework-2-problem-2"
EBS_TAG="Homework"
EBS_TAG_VALUE1="2.1"
EBS_TAG_VALUE2="2.2"

def get_ebs_vol_id(ec2, tag_value):
    response = ec2.describe_volumes(
        Filters=[
            {
                'Name': "tag:" + EBS_TAG,
                'Values': [
                    tag_value
                ]
            },
        ],
    )
    volume_id= response['Volumes'][0]['VolumeId']
    print('***volume:', volume_id)
    return volume_id

def get_instance_id(ec2, tag_value):
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': "tag:" + INSTANCE_TAG,
                'Values': [
                    tag_value
                ],
                'Name': "instance-state-name",
                'Values': [
                    "running"
                ]
            },
        ],
    )
    if (response['Reservations'][0]): 
        instance_id=response['Reservations'][0]['Instances'][0]['InstanceId']
        print('***instance:', instance_id)
        return instance_id

def stop_ec2_instance(ec2, instance_id):
    response = ec2.stop_instances(
        InstanceIds=[instance_id],
    )
    print(f"***stopping instance {instance_id}")
    print(response)

def detach_ebs_vol(ec2, vol_id):
    response = ec2.detach_volume(
        VolumeId=vol_id,
    )
    ec2.get_waiter('volume_available').wait(VolumeIds=[vol_id])
    print(f"***detach ebs vol {vol_id}")
    print(response)

def terminate_ec2_instance(ec2, instance_id):
    response = ec2.terminate_instances(
        InstanceIds=[instance_id],
    )
    print(f"***terminating instance {instance_id}")
    print(response)

def delete_ebs_vol(ec2, vol_id):
    response = ec2.delete_volume(
        VolumeId=vol_id,
    )
    print(f"***deleted volume {vol_id}")
    print(response)

def main():
    ec2 = boto3.client('ec2')
    instance_id = get_instance_id(ec2, INSTANCE_TAG_VALUE)
    volume_id1 = get_ebs_vol_id(ec2, EBS_TAG_VALUE1)
    volume_id2 = get_ebs_vol_id(ec2, EBS_TAG_VALUE2)
    stop_ec2_instance(ec2, instance_id)
    detach_ebs_vol(ec2, volume_id1)
    detach_ebs_vol(ec2, volume_id2)
    terminate_ec2_instance(ec2, instance_id)
    delete_ebs_vol(ec2, volume_id1)
    delete_ebs_vol(ec2, volume_id2)

if __name__ == "__main__":
    main()