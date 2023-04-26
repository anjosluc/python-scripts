import boto3
import json

def add_vpc_statement_to_policy(session, bucket, policy, vpc):
    try:
        statement = {
            "Sid": "VPCUS",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{}/*".format(bucket),
            "Condition": {
                "StringEquals": {
                    "aws:sourceVpc": vpc
                }
            }
        }
        print("Adding policy to {}\n".format(bucket))
        policy['Statement'].append(statement)
        s3_client = session.client("s3")
        s3_client.put_bucket_policy(
            Bucket=bucket,
            Policy=json.dumps(policy)
        )
    except Exception as e:
        print(e)

def bucket_has_policy(bucket):
    try:
        s3_client = session.client("s3")
        policy = json.loads(s3_client.get_bucket_policy(
            Bucket=bucket
        )['Policy'])
        return True
    except Exception as e:
        return False

def list_buckets_with_policy(session, vpc):
    try:
        s3_client = session.client("s3")
        buckets = []
        for item in s3_client.list_buckets()['Buckets']:
            if bucket_has_policy(item['Name']) == True and item['Name'][-3:] != "-nv":
                policy = json.loads(s3_client.get_bucket_policy(
                    Bucket=item['Name']
                )['Policy'])
                add_vpc_statement_to_policy(session, item['Name'], policy, vpc)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    vpc = "vpc-xxxxxxxxxxxx"
    session = boto3.Session(profile_name="default", region_name="sa-east-1")
    list_buckets_with_policy(session, vpc)