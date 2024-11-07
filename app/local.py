# from app.services.ingest_google_font import clone_git_repo, copy_files_by_ext
# from app.services.transform_font import transform_font

from .services.ingest_google_font import clone_git_repo, copy_files_by_ext
from .services.transform_font import transform_fonts


url = "https://github.com/google/fonts"
repo_dir = "./repo"
ttf_dir = "./ttf"
dataset_dir = "./dataset"

clone_git_repo(url, repo_dir)
copy_files_by_ext(repo_dir, ttf_dir, ".ttf")
transform_fonts(ttf_dir, dataset_dir)