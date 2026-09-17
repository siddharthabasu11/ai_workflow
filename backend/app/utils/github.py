import re


def parse_github_url(url: str) -> tuple[str, str]:
    url = url.strip().rstrip("/")

    if url.endswith(".git"):
        url = url[:-4]

    match = re.fullmatch(r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+)", url, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid GitHub repository URL")
    
    owner, name = match.groups()
    return owner.lower(), name.lower()
