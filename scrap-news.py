import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse
from collections import Counter
import re
import json

def fetch_news(hours=1, search_terms=["뉴스"], media_filters=None, sort_order=0, pages=10):
    """
    최신 뉴스 중 사용자가 지정한 시간(hours), 검색어(search_terms), 언론사(media_filters)로 크롤링하는 함수
    """
    search_query = "+".join([f'"{term}"' if "*" in term else term for term in search_terms])
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    now = datetime.now()
    filtered_articles = []
    article_texts = []
    
    print(f"'{ ' '.join(search_terms) }' 검색어로 뉴스 찾는 중...")
    
    for page in range(pages):
        start = page * 10
        url = f"https://www.google.com/search?q={search_query}&tbm=nws&start={start}"
        session = requests.Session()
        response = session.get(url, headers=headers)
        
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".WlydOe")
        
        for article in articles:
            press_tag = article.select_one("div.NUnG9d span")
            press_name = press_tag.text.strip() if press_tag else "알 수 없음"
            
            if media_filters and not any(m in press_name for m in media_filters):
                continue
            
            title_tag = article.select_one("div.n0jPhd")
            title = title_tag.text.strip() if title_tag else "제목 없음"
            
            link_tag = article.get("href")
            link = link_tag if link_tag else "#"
            
            time_tag = article.select_one("div.OSrXXb span")
            time_text = time_tag.text.strip() if time_tag else ""
            
            article_time = parse_relative_time(time_text)
            
            if article_time and now - article_time <= timedelta(hours=hours):
                article_data = {
                    "time": article_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "press": press_name,
                    "title": title,
                    "time_text": time_text,
                    "link": link
                }
                filtered_articles.append(article_data)
                article_texts.append(title)
    
    filtered_articles.sort(key=lambda x: x["time"], reverse=(sort_order == 0))
    
    keywords = analyze_keywords(article_texts)
    save_results(filtered_articles, search_terms, hours, media_filters, sort_order, pages, keywords)

def parse_relative_time(time_text):
    """'2시간 전', '1일 전' 같은 상대 시간을 실제 datetime으로 변환"""
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

def analyze_keywords(texts):
    """뉴스 제목에서 주요 키워드 분석 (3회 이상 등장하는 단어만 포함, 내림차순 정렬)"""
    combined_text = ' '.join(texts)  # 전체 뉴스 제목을 하나의 텍스트로 결합
    words = re.findall(r'\b\w{2,}\b', combined_text)  # 전체 텍스트에서 단어 추출
    
    word_counts = Counter(words)
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)  # 내림차순 정렬
    common_words = [f"{word}->{count}" for word, count in sorted_words if count >= 3]
    
    print("\n📌 주요 키워드 분석:")
    for entry in common_words:
        print(f"- {entry}")
    
    return common_words

def save_results(articles, search_terms, hours, media_filters, sort_order, pages, keywords):
    """ 검색된 뉴스 데이터를 JSON 파일로 저장하며, 기존 데이터에 추가 """
    try:
        with open("news_data.json", "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    
    data_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "search_terms": search_terms,
        "hours": hours,
        "media_filters": media_filters,
        "sort_order": sort_order,
        "pages": pages,
        "articles": articles,
        "keywords": keywords
    }
    
    existing_data.append(data_entry)
    
    with open("news_data.json", "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
    
    print(f"✅ 검색된 뉴스가 'news_data.json'에 저장되었습니다!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="맞춤형 뉴스 크롤링 스크립트")
    parser.add_argument("-t", type=int, default=1, help="최근 몇 시간 내의 뉴스를 가져올지 설정")
    parser.add_argument("-s", type=int, choices=[0, 1], default=0, help="정렬 방식 (0: 최신순, 1: 오래된 순)")
    parser.add_argument("-k", nargs="+", default=["뉴스"], help="검색할 키워드")
    parser.add_argument("-p", type=int, default=10, help="검색할 페이지 수")
    parser.add_argument("-m", nargs="*", default=None, help="특정 언론사 필터링")
    
    args = parser.parse_args()
    fetch_news(hours=args.t, search_terms=args.k, media_filters=args.m, sort_order=args.s, pages=args.p)
