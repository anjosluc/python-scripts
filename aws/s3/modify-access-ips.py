#It ensures that publicIps list are added on sqs policies with ipaddress condition
import boto3
import json
import os
import time


def sqsQueues(session, publicIps): 
    client = session.client("sqs")
    urls = client.list_queues()["QueueUrls"]

    #GET QUEUE URLS
    for url in urls:
        #GET QUEUE POLICY
        policy = client.get_queue_attributes(QueueUrl=url, AttributeNames=['Policy'])
        if 'Attributes' in policy:
            jsonPolicy = json.loads(policy['Attributes']['Policy'])
            statements = json.loads(policy['Attributes']['Policy'])['Statement']
            #GET POLICY STATEMENTS
            for statement in statements:
                #ENSURING THAT POLICY HAS IP ADDRESS CONDITION    
                if statement['Condition']  is not None and 'IpAddress' in statement['Condition']:
                    listIps = statement['Condition']['IpAddress']['aws:SourceIp']
                    for ip in publicIps:
                        if ip not in listIps:
                            #ADDING IPS
                            listIps.append(ip)
                    statement['Condition']['IpAddress']['aws:SourceIp'] = listIps
                    
            jsonPolicy['Statement'] = statements
            print("URL {}".format(url))
            #SETTING POLICY UPDATED
            client.set_queue_attributes(
                QueueUrl=url, 
                Attributes={
                    'Policy':json.dumps(jsonPolicy)
               }
            )
            print("POLICY SET")
        #print("POLICY {}".format(json.dumps(jsonPolicy)))


if __name__ == "__main__":
    #PROFILE NAME ON .aws/credentials with region name set
    session = boto3.Session(profile_name = "default")
    #PUBLIC IPS TO ADD
    publicIps = ["10.0.0.0/8"]
    sqsQueues(session, publicIps)