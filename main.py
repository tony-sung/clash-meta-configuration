import sys

import requests
import yaml
from lxml import etree

headers = {
    'Host': 'raw.githubusercontent.com',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46",
}
proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
url = "https://raw.githubusercontent.com/snakem982/proxypool/main/README.md"


def get_sublink_from_url(url):
    try:
        url_content = requests.get(url, headers=headers, proxies=proxies).text
        content_line = url_content.split("\n")
        for line in content_line:
            if str.startswith(line, "https://raw.githubusercontent.com/snakem982/proxypool/main/clash"):
                sub_link = line.split(" ")[0]
                break
        return sub_link
    except Exception:
        return 'get_sublink_from_url Error'

# get sublink content
def get_content_from_sublink(url):
    try:
        sub_content = requests.get(url, headers=headers, proxies=proxies).text
        return sub_content
    except Exception:
        return 'get_content_from_sublink Error'

# get node from yaml
def get_nodes_from_yaml(sub_content):
    try:
        nodes = yaml.safe_load(sub_content)['proxies']
        return nodes
    except Exception:
        print(f"get_nodes_from_yaml error: {sub_content}")
        return False

if __name__ == "__main__":
    sublink = get_sublink_from_url(url)
    sub_content = get_content_from_sublink(sublink)
    yaml_content_raw = yaml.safe_load(sub_content)
    yaml_content = yaml.safe_load("proxies:")
    yaml_content['proxies'] = yaml_content_raw['proxies']
    yaml_content = yaml.dump(yaml_content)
    open(f'{sys.path[0]}/subscription/clash-meta.yaml', 'w').write(yaml_content)
