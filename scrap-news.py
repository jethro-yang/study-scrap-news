import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import argparse  # CLI 인자 처리

def fetch_news(hours=1, search_terms="반도체"):
    """
    최신 뉴스 중 사용자가 지정한 시간(hours)과 검색어(search_terms)로 크롤링하여 저장하는 함수
    :param hours: 몇 시간 내의 뉴스만 가져올지 설정 (기본값: 1시간)
    :param search_terms: 검색할 키워드 (기본값: "반도체")
    """
    search_query = "+".join(search_terms)  # 검색어들을 '+'로 연결하여 URL에 적용
    url = f"https://www.google.com/search?q={search_query}&tbm=nws"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    
    if response.status_code != 200:
        print("❌ 요청 실패:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select(".SoAPf")  
    print(f"✅ '{' '.join(search_terms)}' 검색어로 {len(articles)}개의 뉴스 블록 발견!")

    now = datetime.now()
    filtered_articles = []
    
    for article in articles:
        # 언론사 정보 가져오기
        press_tag = article.select_one("div.NUnG9d span")
        press_name = press_tag.text.strip() if press_tag else "알 수 없음"

        # 뉴스 제목 가져오기
        title_tag = article.select_one("div.n0jPhd")
        title = title_tag.text.strip() if title_tag else "제목 없음"

        # 업로드 시간 가져오기
        time_tag = article.select_one("div.OSrXXb span")  # 업로드 시간 태그
        time_text = time_tag.text.strip() if time_tag else ""

        # 상대적 시간을 실제 datetime으로 변환
        article_time = parse_relative_time(time_text)

        # 사용자가 지정한 시간 범위 내의 뉴스만 저장
        if article_time and now - article_time <= timedelta(hours=hours):
            # 언론사를 대괄호, 시간을 소괄호로 감싸서 저장
            formatted_content = f"[{press_name}] {title} ({time_text})"
            filtered_articles.append(formatted_content)

    if filtered_articles:
        with open("news_texts_filtered.txt", "a", encoding="utf-8") as file:
            file.write(f"\n=== 실행 시간: {now.strftime('%Y-%m-%d %H:%M:%S')} / 최근 {hours}시간 / 검색어: {' '.join(search_terms)} ===\n")
            file.writelines([f"{article}\n" for article in filtered_articles])

        print(f"✅ 최근 {hours}시간 내 '{' '.join(search_terms)}' 관련 {len(filtered_articles)}개 뉴스가 'news_texts_filtered.txt' 파일에 저장되었습니다!")

def parse_relative_time(time_text):
    """'2시간 전' 같은 상대 시간을 실제 datetime으로 변환"""
    now = datetime.now()
    if "분 전" in time_text:
        minutes = int(time_text.replace("분 전", "").strip())
        return now - timedelta(minutes=minutes)
    elif "시간 전" in time_text:
        hours = int(time_text.replace("시간 전", "").strip())
        return now - timedelta(hours=hours)
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="맞춤형 뉴스 크롤링 스크립트")
    parser.add_argument("hours", type=int, help="최근 몇 시간 내의 뉴스를 가져올지 설정 (정수)")
    parser.add_argument("search_terms", nargs="+", help="검색할 키워드 (여러 개 입력 가능)")

    args = parser.parse_args()
    fetch_news(hours=args.hours, search_terms=args.search_terms)
