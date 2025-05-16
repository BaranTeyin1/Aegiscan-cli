import git
import os

def clone_repo(repo_url: str, clone_dir: str):
    if os.path.exists(clone_dir):
        raise FileExistsError(f"{clone_dir} zaten var")

    print(f"Klonlanıor: {repo_url} -> {clone_dir}")
    git.Repo.clone_from(repo_url, clone_dir)
    return clone_dir
