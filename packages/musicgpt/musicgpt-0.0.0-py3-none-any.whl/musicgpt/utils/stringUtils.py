
def is_local_filepath(url: str) -> bool:
    """
    Check if the given string is a public HTTP/HTTPS URL or local filepath.

    Args:
        url (str): The string to check.

    Returns:
        bool: True if the string is a local filepath, False otherwise.
    """
    if url.startswith("http://") or url.startswith("https://") or url.startswith("www."):
        return False
    return True

