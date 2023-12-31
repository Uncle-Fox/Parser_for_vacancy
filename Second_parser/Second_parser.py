import requests
from bs4 import BeautifulSoup
import fake_useragent
import fake_useragent
import time
import json

def get_links(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&page=1",
        headers={"user-agent":ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        page_count = int(soup.find("div", attrs={"class":"pager"}).find_all("span",recursive=False)[-1].find("a").find("span").text)
    except:
        return
    try:
        for page in range(page_count):
            data = requests.get(
            url=f"https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&page={page}",
            headers={"user-agent":ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
    except Exception as e:
        print(f"{e}")
    time.sleep(1)

    
def get_vacancy(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent":ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class": "vacancy-title"}).text
    except:
        name = ""
    try:
        salary = soup.find(attrs={"data-qa": "vacancy-salary-compensation-type-net"}).text#.replace("\xa0", "")
    except:
        salary = ""
    try:
        tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={"class":"bloko-tag bloko-tag_inline"})]
    except:
        tags = []
    resume = {
        "name": name,
        "salary": salary,
        "skills": tags,
        "link": link
    }
    return resume


if __name__ == "__main__":
    data = []
    for a in get_links("программист Python"):
        data.append(get_vacancy(a))
        time.sleep(1)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False )


# Данный блок выводит в терминал найденные данные в виде  resume = {"name": name,"salary": salary,"skills": tags}

# if __name__ == "__main__":
#     for a in get_links("программист Python"):
#         print(get_vacancy(a))
#         time.sleep(1)