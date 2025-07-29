# Standard library imports
import json
import os
from pathlib import Path

# Third-party imports
import tornado
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join

from amzn_sagemaker_aiops_jupyterlab_extension.utils.pipelines_output_util import (
    _extract_tar_gz,
    _find_output_notebook,
    _get_notebook_content,
)

# Constants
DEFAULT_HOME_DIRECTORY = "/home/sagemaker-user"
HOME_PATH = os.environ.get("HOME", DEFAULT_HOME_DIRECTORY)


def build_url(web_app, endpoint):
    base_url = web_app.settings["base_url"]
    # Remove any trailing slashes
    base_url = base_url.rstrip("/")
    endpoint = endpoint.lstrip("/")
    return url_path_join(base_url, endpoint)


def register_handlers(nbapp):
    web_app = nbapp.web_app
    host_pattern = ".*$"

    # Add debug logging
    nbapp.log.info("Registering handlers for amzn_sagemaker_aiops_jupyterlab_extension")
    nbapp.log.info(f"Base URL: {web_app.settings['base_url']}")

    handlers = [
        (
            build_url(web_app, "/aws/sagemaker/api/pipelines/get-output"),
            PipelinesOutputHandler,
        ),
    ]
    web_app.add_handlers(host_pattern, handlers)


class PipelinesOutputHandler(JupyterHandler):
    """Handler to download and extract output.tar.gz file from user's SageMaker S3 bucket"""

    @tornado.web.authenticated
    async def get(self):
        self.set_header("Content-Type", "application/json")
        try:
            # Get required parameters from query parameters
            pipeline_name = self.get_argument("pipelineName", None)
            step_name = self.get_argument("stepName", None)
            job_name = self.get_argument("jobName", None)

            # Validate required parameters
            if not all([pipeline_name, step_name, job_name]):
                self.set_status(400)
                self.finish(
                    json.dumps(
                        {
                            "error": "Missing required parameters",
                            "details": "pipelineName, stepName, and jobName are required",
                        }
                    )
                )
                return

            # Construct the S3 key path
            s3_key = f"sagemaker-pipelines/{pipeline_name}/{step_name}/output/{job_name}/output/output.tar.gz"

            # Create the target directory path using HOME_PATH from environment
            home_path = os.environ.get("HOME", "/tmp")  # Use /tmp as fallback
            target_dir = Path(home_path) / pipeline_name / step_name
            target_file = target_dir / "output.tar.gz"

            try:
                # Create directories if they don't exist
                target_dir.mkdir(parents=True, exist_ok=True)

                # Download the file from S3
                self.log.info(f"Downloading from: {s3_key}")
                self.log.info(f"Saving to: {target_file}")

                file_content = await _get_notebook_content(s3_key)

                # Save the file to the target location
                with open(target_file, "wb") as f:
                    f.write(file_content)

                # Extract the tar.gz file
                self.log.info(f"Extracting {target_file} to {target_dir}")
                _extract_tar_gz(str(target_file), str(target_dir))

                # Find the output notebook
                notebook_path = _find_output_notebook(target_dir)

                # Remove the tar.gz file after extraction
                if target_file.exists():
                    target_file.unlink()

                response_data = {
                    "success": True,
                    "message": "File downloaded and extracted successfully",
                    "extractedPath": str(target_dir),
                }

                # Add notebook path to response if found
                if notebook_path:
                    response_data["notebookPath"] = notebook_path

                self.set_status(200)
                self.finish(json.dumps(response_data))

            except Exception as e:
                self.log.error(f"Error processing file from S3: {str(e)}")
                # Clean up the downloaded file if it exists
                if target_file.exists():
                    try:
                        target_file.unlink()
                    except Exception as cleanup_error:
                        self.log.error(f"Error cleaning up file: {str(cleanup_error)}")

                self.set_status(500)
                self.finish(
                    json.dumps(
                        {
                            "error": "Error processing file",
                            "details": str(e),
                        }
                    )
                )

        except Exception as e:
            self.log.error(f"Error in PipelinesOutputHandler: {str(e)}")
            self.set_status(500)
            self.finish(
                json.dumps({"error": "Internal server error", "details": str(e)})
            )
