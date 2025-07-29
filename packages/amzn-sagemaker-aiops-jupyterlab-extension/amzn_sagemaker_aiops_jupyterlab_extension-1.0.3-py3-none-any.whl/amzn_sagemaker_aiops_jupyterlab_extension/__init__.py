try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings

    warnings.warn(
        "Importing 'amzn_sagemaker_aiops_jupyterlab_extension' outside a proper installation."
    )
    __version__ = "dev"
import json
from os import path
from pathlib import Path
from .handlers import register_handlers
from aws_embedded_metrics.config import get_config


# Path to the frontend JupyterLab extension assets
def _jupyter_labextension_paths():
    HERE = Path(__file__).parent.resolve()

    with (HERE / "labextension" / "package.json").open(encoding="utf-8") as fid:
        package_json = json.load(fid)

    return [{"src": "labextension", "dest": package_json["name"]}]


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
