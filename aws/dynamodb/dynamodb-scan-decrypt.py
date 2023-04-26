import boto3
import base64

def update_keys_in_us(tb_name, plain_keys, us_session):
    try:
        dynamo_client = us_session.client("dynamodb")
        kms_client = us_session.client("kms")
        for key in plain_keys:
            print('UPDATING {}'.format(key['KEY']))
            alias_kms = "alias/{}".format(key['KMSKEY'])
            binary_encrypted = kms_client.encrypt(
                KeyId=alias_kms,
                Plaintext=key['PASSWORD']
            )['CiphertextBlob']
            print(base64.encodebytes(binary_encrypted))
            key_base64 = base64.encodebytes(binary_encrypted)
            kms_decrypt = kms_client.decrypt(
                CiphertextBlob=base64.decodebytes(key_base64)
            )['Plaintext']
            if str(key['PASSWORD']) == str(kms_decrypt):
                print("KEY PLAIN - {}  /   KEY DECRYPTED: {} ".format(key['PASSWORD'], kms_decrypt))
                update_response = dynamo_client.update_item(
                    TableName=tb_name,
                    ExpressionAttributeNames={
                        '#P': 'PASSWORD'
                    },
                    ExpressionAttributeValues={
                        ':p': {
                            'B': base64.decodebytes(key_base64)
                        }
                    },
                    Key={
                        'KEY': {
                            'S': key['KEY']
                        }
                    },
                    UpdateExpression='SET #P = :p'
                )
                print(update_response)
    except Exception as e:
        raise e


def sp_scan_dynamo(tb_name, br_session):
    try:
        dynamo_client = br_session.client("dynamodb")
        kms_client = br_session.client("kms")
        response = dynamo_client.scan(
            TableName=tb_name
        )['Items']
        keys_plain = []
        for key in response:
            #print(key['KEY'])
            if key['PASSWORD']['B'] != None:
                #print(key['PASSWORD']['B'])
                base64_key = base64.encodebytes(key['PASSWORD']['B'])
                print(base64_key)
                decrypted_key = kms_client.decrypt(
                    CiphertextBlob=base64.decodebytes(base64_key)
                )
                print("DECRYPTED KEY {}: {}".format(key['KEY']['S'], decrypted_key['Plaintext']))
                keys_plain.append({"KEY": str(key['KEY']['S']), "PASSWORD": decrypted_key['Plaintext'], "KMSKEY": str(key['KMSKEY']['S'])})
        return keys_plain
    except Exception as e:
        raise e

def lambda_handler(event, context):
    try:
        br_session = boto3.Session(profile_name=event['profile'], region_name="sa-east-1")
        us_session = boto3.Session(profile_name=event['profile'], region_name="us-east-1")
        plain_keys = sp_scan_dynamo("TABLE", br_session)
        update_keys_in_us("TABLE", plain_keys, us_session)
    except Exception as e:
        raise e

if __name__ == "__main__":
    lambda_handler({"profile": "default"}, {})