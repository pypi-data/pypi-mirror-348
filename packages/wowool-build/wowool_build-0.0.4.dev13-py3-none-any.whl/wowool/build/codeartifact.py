from os import environ
from sys import stderr
from dataclasses import dataclass
from typing import Optional, Union
from pathlib import Path
from subprocess import run
import hashlib
import json
import re
from wowool.build.exceptions import UploadError, DownloadError


@dataclass
class AwsCredentials:
    """
    Credentials to access AWS
    """

    domain: str
    domain_owner: int
    region: str

    @staticmethod
    def from_environment():
        return AwsCredentials(
            domain=environ["AWS_DOMAIN"],
            domain_owner=int(environ["AWS_DOMAIN_OWNER"]),
            region=environ["AWS_REGION"],
        )


@dataclass
class CodeArtifactCredentials:
    """
    Credentials to access a CodeArtifact repository
    """

    repository: str

    @staticmethod
    def from_environment():
        return CodeArtifactCredentials(repository=environ["AWS_CODEARTIFACT_REPOSITORY"])


def _check_not_dirty(fn: Path):
    if "dirty" in fn.name:
        raise UploadError(f"Attempted to upload a dirty version: {fn}")


def upload_pypi(fp: Path, expression: str = "*"):
    """
    Upload a Python package to AWS CodeArtifact
    """
    fp_dist = fp / "dist"
    for fn in fp_dist.glob(expression):
        _check_not_dirty(fn)
        cmd = f"twine upload {fn} --repository codeartifact"
        try:
            run(cmd, shell=True, check=True, cwd=fp)
        except Exception as error:
            raise UploadError(f"AWS CodeArtifact Twine upload failed: {error}")


def _sha256sum(fn: Path):
    with open(fn, "rb", buffering=0) as ifs:
        return hashlib.file_digest(ifs, "sha256").hexdigest()  # pyright: ignore


def delete_raw(
    package: str,
    version: str,
    namespace: str | None = None,
    format: str = "generic",
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
):
    aws = aws or AwsCredentials.from_environment()
    codeartifact = codeartifact or CodeArtifactCredentials.from_environment()
    options = f"--namespace {namespace}" if namespace != None else ""
    options += f" --format {format}"
    cmd = f"""aws codeartifact delete-package-versions --domain {aws.domain} --domain-owner {aws.domain_owner} --region {aws.region} --repository {codeartifact.repository}  {options} --package {package} --versions {version} """
    result = run(cmd, shell=True, check=False, capture_output=True)
    print(result.stdout.decode())
    if result.returncode != 0:
        print(result.stderr.decode(), file=stderr)
        raise UploadError(f"AWS CodeArtifact generic upload failed {cmd=}")


def upload_raw_aws_cli(
    fn: Path,
    namespace: str,
    package: str,
    version: str,
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
    overwrite=False,
):
    fn = Path(fn)
    aws = aws or AwsCredentials.from_environment()
    codeartifact = codeartifact or CodeArtifactCredentials.from_environment()

    if overwrite:
        try:
            delete_raw(namespace=namespace, package=package, version=version)
        except Exception as error:
            print(f"AWS CodeArtifact generic delete failed: {error}", file=stderr)

    try:
        asset_hash = _sha256sum(fn)
    except Exception as error:
        raise UploadError(f"Could not produce sha256 hash for {fn}: {error}")
    try:
        cmd = f"""aws codeartifact publish-package-version --domain {aws.domain} --domain-owner {aws.domain_owner} --region {aws.region} --repository {codeartifact.repository} --format generic --namespace {namespace} --package {package} --package-version {version} --asset-content {fn} --asset-name {fn.name} --asset-sha256 '{asset_hash}' --unfinished"""
        result = run(cmd, shell=True, check=False, capture_output=True)
        print(result.stdout.decode())
        if result.returncode != 0:
            print(result.stderr.decode(), file=stderr)
            raise UploadError(f"AWS CodeArtifact generic upload failed {cmd=}")
    except Exception as error:
        raise UploadError(f"AWS CodeArtifact generic upload failed: {error}")


def upload_raw(
    fn: Path,
    namespace: str,
    package: str,
    version: str,
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
    overwrite=False,
):
    """
    Upload a raw asset to AWS CodeArtifact using boto3
    """
    fn = Path(fn)

    try:
        import boto3
    except ImportError:
        raise UploadError("boto3 is not installed. Please install it to use this function.")

    aws = aws or AwsCredentials.from_environment()
    codeartifact = codeartifact or CodeArtifactCredentials.from_environment()

    # Check if credentials are valid
    try:
        sts_client = boto3.client("sts", region_name=aws.region)
        identity = sts_client.get_caller_identity()
    except Exception as e:
        raise UploadError(f"AWS credential error: {e}")

    # Create CodeArtifact client
    client = boto3.client("codeartifact", region_name=aws.region)

    # Delete existing version if overwrite is True
    if overwrite:
        try:
            client.delete_package_versions(
                domain=aws.domain,
                domainOwner=str(aws.domain_owner),
                repository=codeartifact.repository,
                format="generic",
                namespace=namespace,
                package=package,
                versions=[version],
            )
            print(f"Deleted existing version: {namespace}/{package}@{version}")
        except Exception as error:
            print(f"Note: Could not delete existing version: {error}", file=stderr)

    # Calculate SHA-256 hash
    try:
        with open(fn, "rb", buffering=0) as ifs:
            asset_hash = hashlib.file_digest(ifs, "sha256").hexdigest()
    except Exception as error:
        raise UploadError(f"Could not produce sha256 hash for {fn}: {error}")

    # Read file content
    try:
        with open(fn, "rb") as f:
            file_content = f.read()
    except Exception as error:
        raise UploadError(f"Could not read file {fn}: {error}")

    # Upload the asset
    try:
        # Use publish_package_version instead
        response = client.publish_package_version(
            domain=aws.domain,
            domainOwner=str(aws.domain_owner),
            repository=codeartifact.repository,
            format="generic",
            namespace=namespace,
            package=package,
            packageVersion=version,
            assetContent=file_content,
            assetName=fn.name,
            assetSHA256=asset_hash,
            unfinished=True,
        )

        print(f"Successfully uploaded {fn.name} to {namespace}/{package}@{version}")
        return response
    except Exception as error:
        raise UploadError(f"AWS CodeArtifact upload failed: {error}")


def run_codeartifact(
    cmd: str,
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
):
    aws = aws or AwsCredentials.from_environment()
    codeartifact = codeartifact or CodeArtifactCredentials.from_environment()
    try:
        codeartifact_cmd = f"aws codeartifact {cmd}"
        print(f"Running: {codeartifact_cmd}")
        result = run(codeartifact_cmd, shell=True, check=False, capture_output=True)

        if result.returncode != 0:
            print(result.stderr.decode(), file=stderr)
            raise UploadError(f"AWS CodeArtifact generic cmd failed {cmd=}")
        else:
            return result.stdout.decode()
    except Exception as error:
        raise UploadError(f"AWS CodeArtifact generic cmd failed: {error}")


def download_raw_aws_cli(
    output: Union[str, Path],
    namespace: str,
    package: str,
    version: str,
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
):
    output = Path(output)
    aws = aws or AwsCredentials.from_environment()
    codeartifact = codeartifact or CodeArtifactCredentials.from_environment()
    try:
        cmd = f"""aws codeartifact get-package-version-asset --package-version {version} --domain {aws.domain} --domain-owner {aws.domain_owner} --region {aws.region} --repository {codeartifact.repository} --format generic --namespace {namespace} --package {package} --asset {output.name} {output}"""
        result = run(cmd, shell=True, check=False, capture_output=True)
        print(result.stdout.decode())
        if result.returncode != 0:
            print(result.stderr.decode(), file=stderr)
            raise UploadError(f"AWS CodeArtifact generic upload failed {cmd=}")
    except Exception as error:
        raise UploadError(f"AWS CodeArtifact generic upload failed: {error}")


def download_raw(
    output: Union[str, Path],
    namespace: str,
    package: str,
    version: str,
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
):
    output = Path(output)
    try:
        import boto3
    except ImportError:
        raise UploadError("boto3 is not installed. Please install it to use this function.")

    aws = aws or AwsCredentials.from_environment()
    codeartifact = codeartifact or CodeArtifactCredentials.from_environment()

    # Check if credentials are valid
    sts_client = boto3.client("sts")
    try:
        identity = sts_client.get_caller_identity()
    except Exception as e:
        print(f"AWS credential error: {e}")

    # Get auth token
    client = boto3.client("codeartifact", region_name=aws.region)
    try:
        # Get the asset
        response = client.get_package_version_asset(
            domain=aws.domain,
            domainOwner=str(aws.domain_owner),
            repository=codeartifact.repository,
            format="generic",
            namespace=namespace,
            package=package,
            packageVersion=version,
            asset=output.name,
        )

        # Save to file
        with open(output, "wb") as f:
            f.write(response["asset"].read())

        print(f"Successfully downloaded {output}")

    except Exception as e:
        raise DownloadError(f"Error downloading asset: {str(e)} {output=}")


def iter_packages(expression=".*", aws: Optional[AwsCredentials] = None, codeartifact: Optional[CodeArtifactCredentials] = None):

    exp_ = re.compile(expression)
    cmd = "list-packages --domain wowool --repository wowool --max-items 1000 "
    data = run_codeartifact(cmd, aws, codeartifact)
    jo = json.loads(data)
    for package in jo["packages"]:
        if exp_.search(package["package"]):
            yield package["package"]


def list_package_info(
    expression: str = ".*",
    version_expression: str = ".*",
    aws: Optional[AwsCredentials] = None,
    codeartifact: Optional[CodeArtifactCredentials] = None,
):

    version_exp_ = re.compile(version_expression)
    for name in iter_packages(expression, aws, codeartifact):
        try:
            cmd = f"list-package-versions --domain wowool --repository wowool --format pypi --package {name}"
            jo_version = json.loads(run_codeartifact(cmd))
            # print(jo_version)
            # yield jo_version['defaultDisplayVersion']
            for version in jo_version["versions"]:
                if version_exp_.match(version["version"]):
                    yield jo_version["namespace"], jo_version["package"], version["version"], jo_version["format"]
        except UploadError as error:
            print(f"Error: {error}", file=stderr)
