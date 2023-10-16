import sys

import requests
import yaml
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
}
proxies = {'http': 'http://localhost:7890', 'https': 'http://localhost:7890'}
url_list = {
    'wanshanziwo_clash.meta': {
        'url': 'https://wanshanziwo.eu.org',
        'xpath': '/html/body/div/section[3]/div/table/tbody/tr[4]/td[1]'
    },
    'wanshanziwo_clash': {
        'url': 'https://wanshanziwo.eu.org/clash',
        'xpath': '/html/body/div/section[1]/div/div/table/tbody/tr[2]/td[1]'
    }
}
def get_sublink_from_url(url, xpath):
    try:
        url_content = requests.get(url, headers=headers, proxies=proxies).text
        sub_link = etree.HTML(url_content).xpath(f'{xpath}/text()')[0]
        return(sub_link)
    except Exception:
        print(f"get_sublink_from_url error: {url}\t{xpath}")
        return False
# get sublink content
def get_content_from_sublink(url):
    try:
        sub_content = requests.get(url, headers=headers, proxies=proxies).text
        return sub_content
    except Exception:
        return False
# get node from yaml
def get_nodes_from_yaml(sub_content):
    try:
        nodes = yaml.safe_load(sub_content)['proxies']
        return(nodes)
    except Exception:
        print(f"get_nodes_from_yaml error: {sub_content}")
        return False
# duplicates remove
def duplicate_removel(node_content):
    node_content_duplicated = []
    if 'proxies' in node_content:
        for node in node_content['proxies']:
            if node not in node_content_duplicated:
                node_content_duplicated.append(node)
        node_content['proxies'] = node_content_duplicated
    return node_content
if __name__ == "__main__":
    sub_content_list = []
    for name in url_list:
        sub_link = get_sublink_from_url(url_list[name]['url'],url_list[name]['xpath'])
        if sub_link:
            sub_content = get_content_from_sublink(sub_link)
        if sub_content:
            if 'proxies:' in sub_content:
                node_content = get_nodes_from_yaml(sub_content)
                sub_content_list.extend(node_content)
            else:
                continue
    yaml_content = yaml.safe_load("proxies:")
    yaml_content['proxies'] = sub_content_list
    yaml_content = duplicate_removel(yaml_content)
    sub_content_group = yaml.dump(yaml_content)
    open(f'{sys.path[0]}/subscription/clash-meta.yaml', 'w').write(sub_content_group)