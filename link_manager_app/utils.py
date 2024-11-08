import requests
from bs4 import BeautifulSoup


def fetch_link_metadata(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    metadata = {
        "title": None,
        "description": None,
        "preview_image": None,
        "link_type": "website"
    }

    og_title = soup.find("meta", property="og:title")
    og_description = soup.find("meta", property="og:description")
    og_image = soup.find("meta", property="og:image")
    og_type = soup.find("meta", property="og:type")

    if og_image:
        metadata["preview_image"] = og_image.get("content", None)

    if og_type:
        metadata["link_type"] = og_type.get("content", None)

    if og_title:
        metadata["title"] = og_title.get("content", None)
    elif soup.title:
        metadata["title"] = soup.title.string

    if og_description:
        metadata["description"] = og_description.get("content", None)
    else:
        meta_description = soup.find("meta", {"name": "description"})
        if meta_description:
            metadata["description"] = meta_description.get("content", None)

    return metadata
