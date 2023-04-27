import requests, string, os
from bs4 import BeautifulSoup


def clean_title(title):
    title = title.translate(str.maketrans("", "", string.punctuation))
    title = title.replace(" ", "_")
    return title.strip() + '.txt'


def get_body(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    body = soup.find('p', {"class": "article__teaser"}).text
    return body


def save_article(url, kind, folder):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = soup.find_all('article')
    url_prefix = "https://www.nature.com"
    for i in titles:
        if i.find('span', {'class': 'c-meta__type'}).text != kind:
            continue

        title = i.find('a').text
        file_name = clean_title(title)
        link = i.find('a').get('href')
        file_link = url_prefix + link
        content = get_body(file_link)
        with open(os.path.join(folder, file_name), 'wb') as file:
            file.write(content.encode('utf-8'))


# proxies = {
#    'http': 'http://127.0.0.1:1087',
#    'https': 'https://127.0.0.1:1087'
# }

headers = {
    'accept-language': 'en-US,en;q=0.5',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
}

# print("Input the URL:")
# url = input()
# url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
# r = requests.get(url, headers=headers, proxies=proxies)
# r = requests.get(url, headers=headers)

############################ stage 2
# if r.status_code == 200 and "www.nature.com/articles" in url:
#     soup = BeautifulSoup(r.content, 'html.parser')
#     a = soup.find('title')
#     b = soup.find('meta', {'name': 'description'})
#     res = {"title": a.text, "description": b.get("content")}
#     print(res)
# else:
#     print("Invalid page!")


############################ Stage 3
# if r.status_code == 200:
#     with open('source.html', 'wb') as file:
#         file.write(r.content)
#     print("Content saved.")
# else:
#     print(f"The URL returned {r.status_code}!")

############################ Stage 4


# soup = BeautifulSoup(r.content, 'html.parser')
# titles = soup.find_all('article')
# file_list = []
# url_prefix = "https://www.nature.com"
# for i in titles:
#     if i.find('span', {'class': 'c-meta__type'}).text != 'News':
#         continue
#
#     title = i.find('a').text
#     file_name = clean_title(title)
#     link = i.find('a').get('href')
#     file_link = url_prefix + link
#     content = get_body(file_link)
#     with open(file_name, 'wb') as file:
#         file.write(content.encode('utf-8'))
#     file_list.append(file_name)
#
# print("Saved articles: ", file_list)

############################ Stage 5
base_url = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page="
page, kind = int(input()), input()


for i in range(1, page + 1):
    folder_name = f'Page_{i}'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    url = base_url + str(i)
    save_article(url, kind, folder_name)

print("Saved all articles.")
