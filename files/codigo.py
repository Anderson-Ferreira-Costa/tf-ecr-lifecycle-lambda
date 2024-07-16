import json
import boto3

def lambda_handler(event, context):
    regions = ['us-east-1']
    max_repos = 400
    
    # Read lifecycle policy text from file
    with open('policy.json', "r") as f:
        lifecycle_text = f.read()
    
    for region in regions:
        print("[INFO] Starting verification on Region:", region)
        ecr = boto3.client('ecr', region_name=region)
        
        try:
            # List repositories
            repos = ecr.describe_repositories(maxResults=max_repos)
            
            # Apply lifecycle policy to each repository
            for repo in repos['repositories']:
                print("[INFO] Putting lifecycle policy on repository:", repo['repositoryName'])
                ecr.put_lifecycle_policy(
                    repositoryName=repo['repositoryName'],
                    lifecyclePolicyText=lifecycle_text
                )
        except Exception as e:
            print("[ERROR] Error accessing ECR in region:", region)
            print("[ERROR]", e)
        
        print("[INFO] Verification Ended")
    
    return "Finished"
