import os
from setuptools import setup, find_packages
# autossh -M 0 -R gluer.serveo.net:443:localhost:9001 serveo.net

def get_version_from_tag():
    """
    Retrieves the version from the GitLab CI/CD environment variable.
    Falls back to trying to get it from a local git tag, or a default.
    """
    version = os.environ.get("CI_COMMIT_TAG")  # Get from GitLab variable

    if version:
        return version
    else:
        try:
            from subprocess import check_output
            tag = check_output(["git", "describe", "--tags", "--abbrev=0"]).decode("utf-8").strip()
            if tag:
                return tag
            else:
                return "0.0.0"
        except Exception:
            return "0.0.0"

# Use the function to get the version
version = get_version_from_tag()

setup(
    name="gluerpy",
    version=version,
    packages=find_packages(),
    install_requires=['redis'],  # List your dependencies here
    description="Python library to connect to gluer services",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://www.gluer.io",  # GitHub repo or project page
    author="Thiago Magro",
    author_email="thiago.magro@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
