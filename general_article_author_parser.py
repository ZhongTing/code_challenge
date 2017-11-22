import csv
import re
import socket
import urllib.request
from difflib import SequenceMatcher
from bs4 import BeautifulSoup, NavigableString


def is_contain_url(string):
    url_pattern = ".*https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"
    return re.match(url_pattern, string) is not None


def import_url_from_csv(file_name):
    with open(file_name, 'r') as csv_file:
        url_reader = csv.reader(csv_file)
        urls = [row[0].replace("'", "") for row in url_reader]
        for url in urls:
            if not is_contain_url(url):
                urls.remove(url)
        return urls


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def request_html(url):
    retry_times = 5
    recent_error = None
    while retry_times > 0:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/42.0.2311.90 Safari/537.36 "
            }
            request = urllib.request.Request(url, headers=headers)
            resource = urllib.request.urlopen(request, timeout=10)
            return resource.read()
        except (urllib.error.URLError, socket.timeout) as e:
            recent_error = e
            retry_times -= 1
    raise recent_error


def get_author_str(node):
    unclean_str = node.a.text if node.a else node.text
    string = re.sub("( +)|\n", " ", unclean_str).strip()
    return re.sub("[bB][yY] ", "", string)


def get_max_children_count(node):
    max_children = 0
    for n in node.recursiveChildGenerator():
        if isinstance(n, NavigableString):
            continue
        max_children = len(list(n.children)) if len(list(n.children)) > max_children else max_children
    return max_children


def parse_author_list(soup):
    # method 1 : check meta tag
    for meta_attr in ['property', 'name']:
        author_metas = soup.findAll("meta", attrs={meta_attr: re.compile("author")})
        for author_meta in author_metas:
            author_meta_content = author_meta.attrs["content"]
            if author_meta_content and not is_contain_url(author_meta_content):
                return [author_meta_content]

    # method 2 : find all tag where  contain "author" and exclude "comments"
    # the node contains many children will be excluded too.
    for tag_attr in ['class', 'rel', 'itemprop']:
        author_nodes = []
        for node in soup.findAll(attrs={tag_attr: re.compile("author")}):
            if node.find_parent(attrs={'class': re.compile("comments?")}):
                continue
            if get_max_children_count(node) > 5:
                continue
            if node.findAll(attrs={'class': re.compile("author")}):
                continue
            if not get_author_str(node):
                continue
            node_html_structure = re.sub(">[.\n]*?<", "><", str(node))
            author_nodes.append({"node": node,
                                 "html_structure": node_html_structure,
                                 "author_name": get_author_str(node)})
        # if author's name are the same, return it
        author_set = set([author_node["author_name"] for author_node in author_nodes])
        if len(author_set) == 1:
            return list(author_set)
        # pick up the most unique tag (html structure is not similar to the others)
        author_list = []
        for i in range(len(author_nodes)):
            author_list.append(author_nodes[i])
            for j in range(len(author_nodes)):
                if i is j:
                    continue
                if similar(author_nodes[i]["html_structure"], author_nodes[j]["html_structure"]) > 0.85:
                    author_list.remove(author_nodes[i])
                    break
        if len(author_list) is not 0:
            return [author['author_name'] for author in author_list]
    return []


def main():
    article_urls = import_url_from_csv('articles.csv')
    result_list = []
    for article_url in article_urls:
        try:
            html = request_html(article_url)
            soup = BeautifulSoup(html, "lxml")
            soup.find_all()
            author_list = parse_author_list(soup)
            # assume there is only one author
            author = author_list[0] if len(author_list) > 0 else None
            print(author, len(author_list), article_url)
            result_list.append([author, article_url])
        except Exception as e:
            result_list.append([e, article_url])
            print(e, article_url)

    with open('output.csv', 'w', encoding="utf-8") as output_csv:
        writer = csv.writer(output_csv, lineterminator='\n')
        writer.writerow(["author", "url"])
        for result in result_list:
            writer.writerow(result)


if __name__ == "__main__":
    main()
