import boto3
import json

def delete_images_in_repositories(session):
    ecr_client = br_session.client("ecr")
    repositories = ecr_client.describe_repositories(
        maxResults=500
    )['repositories']
    for repo in repositories:
        if 'statementrepository' in repo['repositoryName']:
            repo_images = ecr_client.list_images(
                repositoryName=repo['repositoryName'],
                maxResults=100
            )
            print(repo['repositoryName'])
            print(len(repo_images['imageIds']))
            while 'nextToken' in repo_images or len(repo_images['imageIds']) > 0:
                if len(repo_images['imageIds']) > 0:
                    print("DELETING FROM {}....".format(repo['repositoryName']))
                    delete_result = ecr_client.batch_delete_image(
                        repositoryName=repo['repositoryName'],
                        imageIds=repo_images['imageIds']
                    )
                    print(delete_result)
                repo_images = ecr_client.list_images(
                    repositoryName=repo['repositoryName'],
                    maxResults=100
                )
                
            ecr_client.delete_repository(
                repositoryName=repo['repositoryName']
            )

if __name__ == "__main__":
    br_session = boto3.Session(profile_name="default", region_name="sa-east-1")
    delete_images_in_repositories(br_session)