import os
import tarfile
from pathlib import Path
from typing import Optional

from async_lru import alru_cache

from amzn_sagemaker_aiops_jupyterlab_extension.clients import get_s3_client
from amzn_sagemaker_aiops_jupyterlab_extension.exceptions import NotebookTooLargeError
from amzn_sagemaker_aiops_jupyterlab_extension.utils.app_metadata import (
    get_aws_account_id,
    get_region_name,
)


def _find_output_notebook(extract_path):
    """
    Find the notebook file that ends with -output.ipynb in the extracted directory
    """
    try:
        # Search recursively for files ending with -output.ipynb
        notebook_files = list(Path(extract_path).rglob("*-output.ipynb"))

        if notebook_files:
            # Return the first matching notebook file
            return str(notebook_files[0])
        return None
    except Exception:
        return None


def _extract_tar_gz(tar_path, extract_path):
    """
    Safely extract tar.gz file to the specified path
    """
    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            # Check for any files that would extract outside the target directory
            for member in tar.getmembers():
                member_path = os.path.join(extract_path, member.name)
                if not os.path.abspath(member_path).startswith(
                    os.path.abspath(extract_path)
                ):
                    raise Exception("Attempted path traversal in tar file")

            # Extract the files
            tar.extractall(path=extract_path)
        return True
    except Exception:
        raise


@alru_cache(maxsize=5, ttl=60)
async def _get_object_size(bucket: str, key: str) -> Optional[int]:
    account_id = get_aws_account_id()
    s3_client = get_s3_client()
    response = await s3_client.head_object(bucket, key, account_id)
    return response.get("ContentLength")


@alru_cache(maxsize=5, ttl=60)
async def _get_notebook_content(key: str):
    print(f"\nStarting _get_notebook_content with key: {key}")
    # Construct the bucket name using the correct SageMaker format
    account_id = get_aws_account_id()
    region = get_region_name()
    bucket = f"sagemaker-{region}-{account_id}"

    object_size = await _get_object_size(bucket, key)

    if not object_size or object_size > 26214400:
        raise NotebookTooLargeError(f"Object {key} is too large to fit into memory")

    response = await get_s3_client().get_object(bucket, key, account_id)

    return response
