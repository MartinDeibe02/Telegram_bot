import requests
from bs4 import BeautifulSoup


def get_news():
    news_url = "https://www.lavozdegalicia.es/coruna/"
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_keys = ['title','news_href']
        
    list_news = [
        {
            news_keys[0]: news.find(class_="a-min-content").text.replace('\n', " ").split('\t')[0].strip(),
            news_keys[1]: news_url+news.find("a").get("href")
        }
        for news in soup.find_all(class_="article-min")]
    
    message = '📰 *NOTICIAS*'
    for i in list_news[:5]:
        message += f"""
        
🔗 [{i['title']}]({i['news_href']})               
        """
    return message