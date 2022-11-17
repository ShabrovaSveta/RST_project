from urllib.parse import urlparse


def get_relative_link(driver):
    url = urlparse(driver.current_url)
    return url.path
