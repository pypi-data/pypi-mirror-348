from logging import getLogger
from os import getcwd
from pathlib import Path
from subprocess import run, CalledProcessError
from typing import Optional, Union
from os import environ

logger = getLogger(__name__)


def _get_repository_path(fp_repo: Optional[Union[str, Path]] = None) -> Path:
    if fp_repo is None:
        return Path(getcwd())
    else:
        return Path(fp_repo).parent if Path(fp_repo).is_file() else Path(fp_repo)


def increment_version(version: str) -> str:
    try:
        parts = version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    except ValueError:
        return version


def make_version(tag: str, nr_commits: int, has_changes: bool):
    postfix = environ.get("WOWOOL_VERSION_POSTFIX", f".dev{nr_commits}+dirty")
    if "dev0" in tag:
        tag = tag.replace(".dev0", "")
        version = f"{tag}.dev{nr_commits}" if has_changes == 0 else f"{tag}{postfix}"
        return version
    else:
        if has_changes == 0:
            if nr_commits == 0:
                return tag
            else:
                tag = increment_version(tag)
                if "WOWOOL_VERSION_POSTFIX" not in environ:
                    version = f"{tag}.dev{nr_commits}"
                else:
                    version = f"{tag}{postfix}"
                return version
        else:
            tag = increment_version(tag)
            version = f"{tag}{postfix}"
            return version


def run_safe(cmd: str, capture_output: bool = True, cwd: Optional[Union[str, Path]] = None) -> str:
    try:
        res = run(cmd, shell=True, check=True, cwd=cwd, capture_output=capture_output)
        return res.stdout.decode("utf-8").strip()
    except CalledProcessError as ex:
        logger.error(f"Error running command: {cmd}")
        logger.error(ex)
        print(ex.stderr.decode("utf-8"))
        print(ex.stderr.decode("utf-8"))
        raise ex


def get_version_info(fp_repo: Optional[Union[str, Path]] = None) -> dict:
    tag = run_safe("git describe --tags --abbrev=0", cwd=fp_repo)
    nr_commits_result = run_safe(f"git log {tag}..HEAD --oneline", cwd=fp_repo)
    nr_commits = len(nr_commits_result.splitlines())
    has_changes = run("git diff --quiet --exit-code HEAD", shell=True).returncode != 0
    return {"tag": tag, "nr_commits": nr_commits, "has_changes": has_changes}


def get_version(fp_repo: Optional[Union[str, Path]] = None) -> str:
    """
    Get the version from the git history of the given repository folder

    :param fp_repo: Optional repository folder. If not provided, the current
                    working directory is used
    """

    fp_repo = _get_repository_path(fp_repo)
    fn_version = fp_repo / "version.txt"
    if fn_version.is_file():
        version = fn_version.read_text().strip()
        return version

    _git_info = get_version_info(fp_repo)
    return make_version(_git_info["tag"], _git_info["nr_commits"], _git_info["has_changes"])


def git_hash(fp_repo: Optional[Union[str, Path]] = None) -> str:
    fp_repo = _get_repository_path(fp_repo)
    result = run("git rev-parse HEAD", capture_output=True, shell=True, check=True, cwd=fp_repo)
    git_hash_rev = result.stdout.decode().strip()
    return git_hash_rev


def upload_raw(repo: str, version: str, file_path: Path, overwrite: bool = False):
    """
    Upload the raw version of the package to the repository
    repo = your-username/your-repo

    Args:
        repo: GitHub repository in format 'username/repo'
        version: Release tag version
        file_path: Path to the file to upload
        overwrite: If True, overwrite existing asset with same name
    """
    import requests

    GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
    file_name = file_path.name

    # ==== STEP 1: Get the release info ====
    release_url = f"https://api.github.com/repos/{repo}/releases/tags/{version}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    release_resp = requests.get(release_url, headers=headers)
    release_resp.raise_for_status()
    release_data = release_resp.json()
    upload_url = release_data["upload_url"].split("{")[0]
    print(f"✅ Found release: {release_data['name']} (ID: {release_data['id']})")

    # ==== STEP 2: Check for existing asset with same name ====
    if overwrite:
        for asset in release_data.get("assets", []):
            if asset["name"] == file_name:
                print(f"Found existing asset '{file_name}' - deleting it first")
                delete_url = f"https://api.github.com/repos/{repo}/releases/assets/{asset['id']}"
                delete_resp = requests.delete(delete_url, headers=headers)
                delete_resp.raise_for_status()
                print(f"✅ Successfully deleted existing asset")
                break

    # ==== STEP 3: Upload the asset ====
    with open(file_path, "rb") as f:
        headers.update({"Content-Type": "application/gzip"})
        params = {"name": file_name}
        upload_resp = requests.post(upload_url, headers=headers, params=params, data=f)
        upload_resp.raise_for_status()

    print(f"✅ Uploaded: {upload_resp.json()['browser_download_url']}")


def download_raw(repo: str, version: str, file_name: str, output_path: Path):
    """
    Download a raw asset from a GitHub release

    Args:
        repo: GitHub repository in format 'username/repo'
        version: Release tag version
        file_name: Name of the asset to download
        output_path: Path where to save the downloaded file
    """
    import requests

    headers = {"Accept": "application/vnd.github.v3+json"}
    if environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"token {environ.get('GITHUB_TOKEN')}"

    # GITHUB_TOKEN = environ.get("GITHUB_TOKEN")
    # headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN is not None else {}

    # ==== STEP 1: Get the release info ====
    release_url = f"https://api.github.com/repos/{repo}/releases/tags/{version}"
    release_resp = requests.get(release_url, headers=headers)
    release_resp.raise_for_status()
    release_data = release_resp.json()
    print(f"📦 Found release: {release_data['name']} (ID: {release_data['id']})")

    # ==== STEP 2: Find the asset ====
    asset_id = None
    for asset in release_data.get("assets", []):
        if asset["name"] == file_name:
            asset_id = asset["id"]
            print(f"📄 Found asset: {file_name} (ID: {asset_id})")
            break

    if not asset_id:
        available_assets = ", ".join([asset["name"] for asset in release_data.get("assets", [])])
        raise ValueError(f"Asset '{file_name}' not found in release. Available assets: {available_assets}")

    # ==== STEP 3: Download the asset ====
    download_url = f"https://api.github.com/repos/{repo}/releases/assets/{asset_id}"
    download_headers = headers.copy()
    download_headers.update({"Accept": "application/octet-stream"})

    print(f"Downloading from: {download_url}")
    download_resp = requests.get(download_url, headers=download_headers, stream=True)
    download_resp.raise_for_status()

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    with open(output_path, "wb") as f:
        for chunk in download_resp.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Downloaded {file_name} to {output_path}")
    return output_path
