import re


def get_version():
    with open("pyproject.toml", "r") as f:
        content = f.read()
    # Regex to match the version key (assuming it's under [tool.poetry] or similar structure)
    match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if match:
        return match.group(1)
    raise ValueError("Version not found in pyproject.toml")


print(get_version())
