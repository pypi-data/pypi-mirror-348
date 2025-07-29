import json
from os import path
from pathlib import Path
from .handlers import register_handlers
from aws_embedded_metrics.config import get_config

try:
    from ._version import __version__
except ImportError:
    __version__ = "dev"

HERE = Path(__file__).parent.resolve()

# Handle missing labextension directory gracefully
try:
    with (HERE / "labextension" / "package.json").open(encoding="utf-8") as fid:
        data = json.load(fid)
except (FileNotFoundError, json.JSONDecodeError):
    data = {"name": "@amzn/amzn_sagemaker_aiops_jupyterlab_extension"}


# Path to the frontend JupyterLab extension assets
def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": data["name"]}]


def _jupyter_server_extension_points():
    return [
        {
            "module": "amzn_sagemaker_aiops_jupyterlab_extension",
        }
    ]


# Entrypoint of the server extension
def _load_jupyter_server_extension(nb_app):
    nb_app.log.info(f"Loading SageMaker JupyterLab server extension {__version__}")

    # configure EMF logger
    emf_config = get_config()
    emf_config.namespace = "StudioAIOpsJupyterLabExtensionServer"

    register_handlers(nb_app)


load_jupyter_server_extension = _load_jupyter_server_extension
