
import requests
from bs4 import BeautifulSoup

def split_by_uppercase(text):
    words = []
    current_word = ""

    for char in text:
        if char.isupper():
            if current_word:
                words.append(current_word)
                current_word = char
            else:
                current_word = char
        else:
            current_word += char

    if current_word:
        words.append(current_word)

    return words

def parse(text: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com"}
    
    url = f"https://www.beesona.pro/songs/?search={text}"
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "lxml")
    
    song = soup.find("a", href=lambda href: href and not href.startswith("/songs/?") and href.startswith("/songs/") and href != "/songs/")
    urlOfSong = "https://www.beesona.pro" + song.get('href')
    
    html = requests.get(urlOfSong, headers=headers).content
    soup = BeautifulSoup(html, "lxml")
    txt = soup.find("div", {"class":"copys"}).find("div").text.split("@")[0]
    
    txt = txt.replace("\n", " ")  # Заменим все символы переноса строки на пробел
    txt = ' '.join(txt.split())  # Уберем лишние пробелы
    
    out = []
    n = 0
    for i, el in enumerate(split_by_uppercase(txt)):
        if i == 0:
            continue
        if el[0].isupper():
            out.append(" ".join(split_by_uppercase(txt)[n:i]))
            n = i

    return "\n".join(out)

def main():
    print(parse("Трудный возраст"))

if __name__ == '__main__':
    main()
