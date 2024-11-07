import os
import subprocess
import shutil

# from google.cloud.storage import Client
from app.helpers.gcs import upload_dir_to_gcs


def clone_git_repo(url: str, target_dir: str) -> bool:
    command = f"git clone {url} {target_dir}"
    process = subprocess.run(command, shell=True)
    return process.returncode == 0


def copy_files_by_ext(source_dir: str, target_dir: str, ext: str = ".ttf") -> None:
    for root, _, filenames in os.walk(source_dir):
        for filename in filenames:
            if not filename.endswith(ext):
                continue
            source_path = os.path.join(root, filename)
            target_path = os.path.join(target_dir, filename)
            shutil.copyfile(source_path, target_path)


def ingest_google_font(
    repo_dir: str, tff_dir: str, bucket_name: str, prefix: str = "/raw/google_fonts"
):
    url = "https://github.com/google/fonts"
    clone_git_repo(url, repo_dir)
    copy_files_by_ext(repo_dir, tff_dir, ".tff")
    upload_dir_to_gcs(
        tff_dir,
        bucket_name,
        prefix,
    )
