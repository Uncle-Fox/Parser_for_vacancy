import requests

st_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
st_accept_encoding = "gzip, deftate, br"
st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36"
headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent,
    "Accept-Enciding": st_accept_encoding
}

req = requests.get("https://hh.ru/search/vacancy?text=программист+Python&salary=&ored_clusters=true&page=1", headers)
src = req.text
file = open('new_Html', 'w')
file.write(src)
print(src)