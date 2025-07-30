from astrafy_environment import AstrafyEnvironment

gcs_bucket_managed_folder_path = AstrafyEnvironment.bucket_folder_results + "/dp-" + AstrafyEnvironment.data_product.lower()

def upload_to_gcs() -> str:
    return f"""
    gcloud storage cp /app/target/*.json gs://gcs_bucket_managed_folder_path/
    """

def download_failed_models() -> str:
    return f"""
    mkdir -p /app/target
    gcloud storage cp -r gs://gcs_bucket_managed_folder_path/* /app/target/
    """