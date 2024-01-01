import requests
from bs4 import BeautifulSoup
import fake_useragent
import fake_useragent
import time
import json
import logging
import re

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")


def get_links(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        #url=f"https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&page=1",
        url=f"https://hh.ru/search/vacancy?ored_clusters=true&area=113&search_field=name&search_field=company_name&search_field=description&text={text}&enable_snippets=false&L_save_area=true&page=1",
        headers={"user-agent":ua.random}
    )
    if data.status_code != 200:
        logging.error("An ERROR str 27")
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        page_count = int(soup.find("div", attrs={"class":"pager"}).find_all("span",recursive=False)[-1].find("a").find("span").text)
        print(f"Всего нашлось страниц: {page_count}")
    except:
        return
    try:
        for page in range(page_count):
            data = requests.get(
            #url=f"https://hh.ru/search/vacancy?text={text}&salary=&ored_clusters=true&page={page}",
            url=f"https://hh.ru/search/vacancy?ored_clusters=true&area=113&search_field=name&search_field=company_name&search_field=description&text={text}&enable_snippets=false&L_save_area=true&page={page}",
            headers={"user-agent":ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
    except Exception as e:
        print(f"{e}")
    time.sleep(0.25)

    
def get_vacancy(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent":ua.random}
    )
    if data.status_code != 200:
        logging.error("An ERROR str 58")
        return
    soup = BeautifulSoup(data.content, "lxml")
    # try:
    #     number = soup.find("h1", class_="bloko-header-section-3", attrs={"data-qa": "bloko-header-3"}).text
    #     total_number = int(''.join(filter(str.isdigit, number)))
    #     print(f"{number} and {total_number}")
    # except:
    #     total_number = ""
    #     print(f"не удалось найти общее кол-во")
    try:
        name = soup.find(attrs={"class": "vacancy-title"}).text
    except:
        name = ""
    try:
        salary = soup.find(attrs={"data-qa": "vacancy-salary-compensation-type-net"}).text#.replace("\xa0", "")
    except:
        salary = ""
    try:
        company =  soup.find(attrs={"class": "vacancy-company-name"}).text
    except:
        company = ""
    try:
        city =  soup.find("p", attrs={"data-qa": "vacancy-view-location"}).text
    except:
        city = ""
    try:
        adress =  soup.find("span", attrs={"data-qa": "vacancy-view-raw-address"}).text
    except:
        adress = ""
    try:
        tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={"class":"bloko-tag bloko-tag_inline"})]
    except:
        tags = []
    resume = {
        "name": name,
        "salary": salary,
        "company": company,
        "adress": adress,
        "city": city,
        "skills": tags,
        "link": link
    }
    return resume


if __name__ == "__main__":
    logging.info("Program started successfully")
    data_first = []
    data_second = []
    count = 1
    #print("Найдено вакансий: {total_number} \nПримерное время ожидания: {total_number/2}")
    for a in get_links("программист+python+junior"):
        data_first.append(get_vacancy(a))
        #time.sleep(0.25)
        logging.info(f"Correct number {count}")
        count += 1
        with open("data_Python.json", "w", encoding="utf-8") as f:
            json.dump(data_first,f,indent=4,ensure_ascii=False )
    f.close()
    
    for a in get_links("программист+Java+junior"):
        data_second.append(get_vacancy(a))
        #time.sleep(0.25)
        logging.info(f"Correct number {count}")
        count += 1
        with open("data_Java.json", "w", encoding="utf-8") as j:
            json.dump(data_second,j,indent=4,ensure_ascii=False )
    j.close()


# Данный блок выводит в терминал найденные данные в виде  resume = {"name": name,"salary": salary,"skills": tags}

# if __name__ == "__main__":
#     for a in get_links("программист Python"):
#         print(get_vacancy(a))
#         time.sleep(1)