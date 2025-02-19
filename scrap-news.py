import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_news():
    url = "https://www.google.com/search?q=반도체+뉴스&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    print(response.text)

    articles = []
    now = datetime.now()
    
    # 뉴스 리스트 크롤링
    for item in soup.select(".am3QBf"):  # 개별 뉴스 블록 선택
        title_tag = item.select_one(".rQMQod.Xb5VRe")  # 기사 제목
        press_tag = item.select_one(".rQMQod.aJyiOc")  # 언론사
        time_tag = item.select_one(".r0bn4c.rQMQod")   # 업로드 시간
        link_tag = item.select_one("a")  # 기사 링크

        if title_tag and press_tag and time_tag and link_tag:
            title = title_tag.text.strip()
            press = press_tag.text.strip()
            time_text = time_tag.text.strip()
            link = "https://www.google.com" + link_tag["href"]

            # 상대적 시간을 실제 datetime으로 변환
            article_time = parse_relative_time(time_text)
            
            # 30분 이내 뉴스만 저장
            if article_time and now - article_time <= timedelta(minutes=30):
                articles.append((title, press, time_text, link))

    # 파일로 저장
    with open("semiconductor_news.txt", "a", encoding="utf-8") as f:
        f.write(f"\n=== {now.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        for title, press, time_text, link in articles:
            f.write(f"[{time_text}] {press} - {title}\n{link}\n")

    print(f"✅ {len(articles)}개 뉴스 저장 완료!")

def parse_relative_time(time_text):
    """'2시간 전' 같은 상대 시간을 실제 datetime으로 변환"""
    now = datetime.now()

    if "분 전" in time_text:
        minutes = int(time_text.replace("분 전", "").strip())
        return now - timedelta(minutes=minutes)
    elif "시간 전" in time_text:
        hours = int(time_text.replace("시간 전", "").strip())
        return now - timedelta(hours=hours)
    elif "일 전" in time_text:
        days = int(time_text.replace("일 전", "").strip())
        return now - timedelta(days=days)
    
    return None

fetch_news()
