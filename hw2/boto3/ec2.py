import boto3
from botocore.exceptions import ClientError

KEY_PAIR="aws-hw-keypair"
MY_IP="73.93.72.74/32"
SSH_SECURITY_GROUP="SSH-ONLY"
UBUNTU_IMAGE="ami-03f65b8614a860c29"
INSTANCE_TAG="Name"
INSTANCE_TAG_VALUE="ucscx-homework-2-part-2"
EBS_TAG="Homework"
EBS_TAG_VALUE1="2.1"
EBS_TAG_VALUE2="2.2"

# Not used. Reuse Security Group from problem 1
def create_security_group (ec2):
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=SSH_SECURITY_GROUP,
                                            Description='only allow ssh',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('***Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': MY_IP}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

def create_ebs_volume(ec2):
    try:
        response = ec2.create_volume(
            AvailabilityZone='us-west-2a',
            Size=1,
            VolumeType='gp3',
            TagSpecifications=[
                {
                    'ResourceType': "volume",
                    'Tags': [
                        {
                            'Key': EBS_TAG,
                            'Value': EBS_TAG_VALUE2
                        },
                    ]
                },
            ],
        )
        volume_id= response['VolumeId']
        print('***volume:', volume_id)

        ec2.get_waiter('volume_available').wait(VolumeIds=[volume_id])

        print('***Success!! volume:', volume_id, 'created...')
        return volume_id
    except ClientError as e:
        print(e)

def new_ec2_instance(ec2, security_group_id):

    ec2 = boto3.client('ec2', region_name='us-west-2')
    try:
        response = ec2.run_instances(
            ImageId=UBUNTU_IMAGE, 
            MinCount=1, 
            MaxCount=1,
            Placement={
                'AvailabilityZone': 'us-west-2a',
            },
            InstanceType='t2.micro', 
            KeyName=KEY_PAIR,
            SecurityGroupIds=[security_group_id],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags':[
                        { 
                            'Key': INSTANCE_TAG,
                            'Value': INSTANCE_TAG_VALUE
                        },
                    ]
                },
            ],
        )

        instance_id = response['Instances'][0]['InstanceId']
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        print(f"***Created instance {instance_id}")
        return instance_id
    except ClientError as e:
        print(e)
    
def attach_ebs_to_instance(ec2, instance_id, volume_id):

    try:
        response = ec2.attach_volume(
            Device="/dev/xvdg",
            InstanceId=instance_id,
            VolumeId=volume_id)

        ec2.get_waiter('volume_in_use').wait(VolumeIds=[volume_id])
        print('***Success!! volume:', volume_id, 'is attached to instance:', instance_id)

    except Exception as e:
        print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
        print(type(e), ':', e)

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

def main():
    ec2 = boto3.client('ec2')
    instance_id = new_ec2_instance(ec2, SSH_SECURITY_GROUP)
    volume_id2 = create_ebs_volume(ec2)
    volume_id2 = get_ebs_vol_id(ec2, EBS_TAG_VALUE2)
    volume_id1 = get_ebs_vol_id(ec2, EBS_TAG_VALUE1)
    attach_ebs_to_instance(ec2, instance_id, volume_id1)
    attach_ebs_to_instance(ec2, instance_id, volume_id2)

if __name__ == "__main__":
    main()
