import json
import boto3
import os

def list_ecr_repos(br_ecr_client):
    repos = br_ecr_client.describe_repositories()['repositories']
    print("Found {} repos to migrate in sa-east-1...".format(len(repos)))
    return repos

def create_ecr_repos(us_ecr_client, repos):    
    try:
        #GETTING REPOS CREATED IN US 
        us_repos_already_created = []
        for repo in us_ecr_client.describe_repositories()['repositories']:
            us_repos_already_created.append(repo['repositoryName'])

        for repo in repos:
            if repo['repositoryName'] not in us_repos_already_created:
                project_tag = ""
                if "bwp" in repo['repositoryName']:
                    project_tag = "ClientPortal" 
                elif "efs" in repo['repositoryName']:
                    project_tag = "EFS"
                elif "statementrepository" in repo['repositoryName']:
                    project_tag = "ClientTools"

                print("Creating {} in us-east-1...".format(repo['repositoryName']))
                repo_created = us_ecr_client.create_repository(
                    repositoryName=repo['repositoryName'],
                    imageTagMutability=repo['imageTagMutability'],
                    tags=[
                        {
                            'Key': 'Project',
                            'Value': project_tag
                        }
                    ]
                )
                print("Created {} in us-east-1!".format(repo_created['repository']['repositoryUri']))
            else:
                print("Skipping {} creation since is already created...".format(repo['repositoryName']))
        return True
    except Exception as e:
        print("There was an error creating some repo: {}".format(e))
        return False

def lambda_handler(event, context):
    br_ecr_client = boto3.Session(profile_name="digital-uat", region_name="sa-east-1").client("ecr")
    us_ecr_client = boto3.Session(profile_name="digital-uat", region_name="us-east-1").client("ecr")
    ecr_repos = list_ecr_repos(br_ecr_client)
    check_repos_created = create_ecr_repos(us_ecr_client, ecr_repos)
    if check_repos_created:
        print("EVERYTHING WAS OK!!!")

if __name__ == "__main__":
    lambda_handler({}, [])