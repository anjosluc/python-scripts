import boto3

def copy_replace(session, bucket):
    try:
        client = session.client("s3")
        objects = client.list_objects_v2(
            Bucket=bucket,
            MaxKeys=100000,
        )
        next_token = objects['NextContinuationToken']
        keys_s3 = []
        
        while next_token is not None:
            for file in objects['Contents']:
                keys_s3.append(file['Key'])
            
            objects = client.list_objects_v2(
                Bucket=bucket,
                MaxKeys=1000,
                ContinuationToken=next_token
            )
            
            if 'NextContinuationToken' not in objects:
                break
            else:
                next_token = objects['NextContinuationToken']
        
        print(len(keys_s3))
        i = 0
        keys_s3 = keys_s3[49467:]
        for key in keys_s3:
            key_metadata=client.head_object(Bucket=bucket,Key=key)["Metadata"]
            print("{}/{}".format(i + 1, len(keys_s3)))
            if 'key' not in key_metadata:
                key_metadata['key'] = key
                print("{}/{} - copy key {}".format(i + 1, len(keys_s3), key))
                client.copy_object(
                    Bucket=bucket,
                    CopySource="{}/{}".format(bucket, key),
                    Key=key,
                    Metadata=key_metadata,
                    MetadataDirective='REPLACE'
                )
            i+=1
            
    except print(0):
        pass


if __name__ == '__main__':
    session = boto3.Session(profile_name="default", region_name="sa-east-1")
    copy_replace(session, "test_bucket")
    