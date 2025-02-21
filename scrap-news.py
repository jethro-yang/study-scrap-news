import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse
from collections import Counter
import re

def fetch_news(hours=1, search_terms=["뉴스"], media_filters=None, sort_order=0, pages=10):
    """
    최신 뉴스 중 사용자가 지정한 시간(hours), 검색어(search_terms), 언론사(media_filters)로 크롤링하는 함수
    :param hours: 몇 시간 내의 뉴스만 가져올지 설정 (기본값: 1시간)
    :param search_terms: 검색할 키워드 (기본값: ["뉴스"])
    :param media_filters: 특정 언론사 필터링 리스트 (기본값: None = 전체 언론사)
    :param sort_order: 정렬 방식 (0: 최신순, 1: 오래된 순)
    :param pages: 검색할 페이지 수 (기본값: 10페이지)
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
            link = f"Link->{link_tag}" if link_tag else "#"
            
            time_tag = article.select_one("div.OSrXXb span")
            time_text = time_tag.text.strip() if time_tag else ""
            
            article_time = parse_relative_time(time_text)
            
            if article_time and now - article_time <= timedelta(hours=hours):
                formatted_content = (article_time, f"[{press_name}] {title} ({time_text})\n    {link}\n")
                filtered_articles.append(formatted_content)
                article_texts.append(title)
    
    filtered_articles.sort(key=lambda x: x[0], reverse=(sort_order == 0))
    
    if filtered_articles:
        with open("news_texts_filtered.txt", "a", encoding="utf-8") as file:
            file.write(f"\n=== 실행 시간: {now.strftime('%Y-%m-%d %H:%M:%S')} / 최근 {hours}시간 / 검색어: {' '.join(search_terms)} ===\n")
            file.writelines([f"{article[1]}\n" for article in filtered_articles])
        
        print(f"✅ 최근 {hours}시간 내 '{' '.join(search_terms)}' 관련 {len(filtered_articles)}개 뉴스가 'news_texts_filtered.txt' 파일에 저장되었습니다!")
    
    # 키워드 분석
    analyze_keywords(article_texts)

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
    """뉴스 제목에서 주요 키워드 분석"""
    words = []
    for text in texts:
        words.extend(re.findall(r'\b\w{2,}\b', text))  # 단어 추출 (2글자 이상)
    
    word_counts = Counter(words)
    common_words = word_counts.most_common(10)  # 상위 10개 키워드
    
    print("\n📌 주요 키워드 분석:")
    for word, count in common_words:
        print(f"- {word}: {count}회")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="맞춤형 뉴스 크롤링 스크립트")
    parser.add_argument("-t", type=int, default=1, help="최근 몇 시간 내의 뉴스를 가져올지 설정 (정수, 기본값: 1)")
    parser.add_argument("-s", type=int, choices=[0, 1], default=0, help="정렬 방식 (0: 최신 기사 우선, 1: 오래된 기사 우선)")
    parser.add_argument("-k", nargs="+", default=["뉴스"], help="검색할 키워드 (여러 개 입력 가능, 기본값: '뉴스')")
    parser.add_argument("-p", type=int, default=10, help="검색할 페이지 수 (기본값: 10 페이지)")
    parser.add_argument("-m", nargs="*", default=None, help="특정 언론사 필터링 (예: '연합', '조선', '중앙')")
    
    args = parser.parse_args()
    fetch_news(hours=args.t, search_terms=args.k, media_filters=args.m, sort_order=args.s, pages=args.p)
