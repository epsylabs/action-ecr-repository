import os

import boto3 as boto3


def main():
    repository_name = os.getenv("INPUT_NAME")
    region = os.getenv("INPUT_REGION")
    scan_on_push = os.getenv("INPUT_SCAN_ON_PUSH")
    image_tag_mutability = os.getenv("INPUT_IMAGE_TAG_MUTABILITY")

    ecr = boto3.client("ecr")

    try:
        response = ecr.describe_repositories(
            repositoryNames=[
                repository_name,
            ],
        )
        repository = next(iter(response.get("repositories")), None)
    except ecr.exceptions.RepositoryNotFoundException as e:
        response = ecr.create_repository(
            repositoryName=repository_name,
            imageTagMutability=image_tag_mutability,
            imageScanningConfiguration={
                'scanOnPush': bool(scan_on_push)
            }
        )
        repository = response.get("repository")

    repository_url = repository.get("repositoryUri")

    print(f"::set-output name=repository::{repository_url}")


if __name__ == "__main__":
    main()
