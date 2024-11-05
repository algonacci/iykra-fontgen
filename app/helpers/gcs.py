import subprocess


def upload_dir_to_gcs(source_dir: str, bucket_name: str, prefix: str) -> bool:
    # client = Client()
    # bucket = client.bucket(bucket_name)
    # blob = bucket.blob("")
    # blob.upload_from_filename()

    target = f"gs://{bucket_name}/{prefix}/"
    command = f"gcloud storage rsync {source_dir} {target}"
    process = subprocess.run(command, shell=True)
    return process.returncode == 0


def download_dir_from_gcs(bucket_name: str, prefix: str, target_dir: str) -> bool:
    source = f"gs://{bucket_name}/{prefix}/"
    command = f"gcloud storage rsync {source} {target_dir}"
    process = subprocess.run(command, shell=True)
    return process.returncode == 0
