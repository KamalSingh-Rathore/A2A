


import requests, zipfile
from io import BytesIO

def download_github_repo_as_zip(repo_url, extract_to="./repo"):
    # Convert GitHub repo URL to ZIP URL
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]
    zip_url = repo_url.replace("github.com", "github.com") + "/archive/refs/heads/main.zip"

    response = requests.get(zip_url)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted repo to: {extract_to}")




download_github_repo_as_zip("https://github.com/jpxoi/send_whatsapp")
