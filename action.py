import os

import boto3 as boto3


def main():
    repository_name = os.environ["INPUT_NAME"]
    region = os.environ["INPUT_REGION"]
    scan_on_push = os.environ["INPUT_SCAN_ON_PUSH"]
    image_tag_mutability = os.environ["INPUT_IMAGE_TAG_MUTABILITY"]

    ecr = boto3.client("ecr")

    response = ecr.describe_repositories(
        repositoryNames=[
            'repository_name',
        ],
    )

    repository = next(iter(response.get("repositories")), None)

    if not repository:
        response = ecr.create_repository(
            repositoryName=repository_name,
            imageTagMutability=image_tag_mutability,
            imageScanningConfiguration={
                'scanOnPush': bool(scan_on_push)
            }
        )
        repository = response.get("repository")

    repository_url = repository.get("repositoryUri")

    print(response)
    print(f"::set-output name=repositry::{repository_url}")


if __name__ == "__main__":
    main()
