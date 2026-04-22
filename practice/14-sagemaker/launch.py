"""
Launch a SageMaker XGBoost training job (script mode).

Install (SDK v2 only — see requirements.txt):  pip install -r requirements.txt

Training code must live in container_source/ without a requirements.txt there:
if source_dir includes requirements.txt, SageMaker pip-installs it inside the
training image and can break numpy/scipy/xgboost (ImportError: numpy.core.multiarray).

Do not name any local file sagemaker.py (it shadows the real package).

Optional environment variables (local / CI / non-Studio):
  SAGEMAKER_ROLE_ARN — IAM role ARN SageMaker assumes for the job (required if
    get_execution_role() is unavailable).
  SAGEMAKER_DEFAULT_BUCKET — S3 bucket for input/output prefixes; if unset,
    the session default bucket is used (see sagemaker.Session.default_bucket).
"""
import os
from pathlib import Path

import sagemaker
from sagemaker.estimator import Estimator

# Correct submodule (do NOT use: from sagemaker import image_uris — often fails).
from sagemaker.image_uris import retrieve

_HERE = Path(__file__).resolve().parent
# Only training script(s) — never the repo's requirements.txt for the SDK.
_SOURCE = str(_HERE / "container_source")

sess = sagemaker.Session()
region = sess.boto_session.region_name

_env_role = (os.environ.get("SAGEMAKER_ROLE_ARN") or "").strip()
role = _env_role if _env_role else sagemaker.get_execution_role()

_env_bucket = (os.environ.get("SAGEMAKER_DEFAULT_BUCKET") or "").strip()
bucket = _env_bucket if _env_bucket else sess.default_bucket()

train_s3 = f"s3://{bucket}/sagemaker/xgboost/train/"
# Model tarball and logs: SageMaker writes under this prefix (job name is appended by the service).
output_path = f"s3://{bucket}/sagemaker/xgboost/output/"

instance_type = "ml.m5.large"
framework_version = "1.7-1"  # if retrieve() fails in your Region, try "1.5-1"

image_uri = retrieve(
    framework="xgboost",
    region=region,
    version=framework_version,
    py_version="py3",
    image_scope="training",
    instance_type=instance_type,
)

estimator = Estimator(
    image_uri=image_uri,
    entry_point="train.py",
    source_dir=_SOURCE,
    role=role,
    output_path=output_path,
    instance_count=1,
    instance_type=instance_type,
    sagemaker_session=sess,
    hyperparameters={
        "max_depth": 5,
        "eta": 0.2,
        "objective": "multi:softmax",
        "num_class": 3,
        "num_round": 20,
    },
)

fit_result = estimator.fit({"train": train_s3})
print("fit() result:", fit_result)

job = estimator.latest_training_job
print("Training job name:", job.name)
print("Training job status:", job.describe().get("TrainingJobStatus"))
print("Model artifact S3 URI (model.tar.gz):", estimator.model_data)
print(
    "Full job details (including the CloudWatch log stream): "
    "in the SageMaker console, open Training → Training jobs and select this job."
)
