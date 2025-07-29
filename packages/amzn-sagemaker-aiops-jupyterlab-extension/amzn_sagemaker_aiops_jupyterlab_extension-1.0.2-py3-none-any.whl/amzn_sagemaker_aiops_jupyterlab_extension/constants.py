# Common Constants
LOGFILE_ENV_NAME = "SAGEMAKER_AIOPS_LOG_FILE"
SCHEMAS_DIR = "schemas/"

# Jupyter Server constants for Log files and schema
SERVER_LOG_FILE_NAME = "sm-aiops-jupyter-server-ext.log"
API_LOG_FILE_NAME = "sm-aiops-jupyter-server-ext.api.log"
REQUEST_LOG_FILE_NAME = "sm-aiops-jupyter-server-ext.requestss.log"
SERVER_LOG_SCHEMA = "http://sagemaker.studio.jupyterserver.log.schema"
HANDLER_METRICS_SCHEMA = "http://sagemaker.studio.jupyterserver.api.metric.schema"
REQUEST_METRICS_SCHEMA = (
    "http://sagemaker.studio.jupyterserver.httprequest.metric.schema"
)

# JupyterLab constants for Log files and schema
JUPYTERLAB_OPERATION_LOG_FILE_NAME = "sm-aiops-jupyterlab-ext.ui.log"
JUPYTERLAB_METRICS_LOG_FILE_NAME = "sm-aiops-jupyterlab-ext.ui.metrics.log"
JUPYTERLAB_OPERATIONAL_LOG_SCHEMA = "http://sagemaker.studio.jupyterlab.ui.log.schema"
JUPYTERLAB_PERFORMANCE_METRICS_LOG_SCHEMA = (
    "http://sagemaker.studio.jupyterlab.ui.performance.schema"
)

CONTEXT_INJECT_PLACEHOLDER = "__INJECT__"
DEFAULT_HOME_DIRECTORY = "/home/sagemaker-user"
