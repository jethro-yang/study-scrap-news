# 사용법
- 기본
  - 시간: 1시간
  - 정렬: 내림차순
  - 검색어: 뉴스
  - 페이지: 10페이지
```
python .\scrap-news.py
```
- 파라미터
  - -t: 시간 hours
  - -s: 정렬
    - 0: 내림차순
    - 1: 오름차순
  - -k: 키워드
    - 예시1: 반도체
    - 예시2: 반도체 삼성
  - -p: 페이지: 정수값
```
python .\scrap-news.py -t 2 -s 1 -k 삼성 반도체
```
---

# 결과 값
```
python .\scrap-news.py -t 3 -s 0 -k 반도체 
✅ '반도체' 검색어로 22개의 뉴스 블록 발견!
✅ 최근 3시간 내 '반도체' 관련 7개 뉴스가 'news_texts_filtered.txt' 파일에 저장되었습니다!

// news_texts_filtered.txt
=== 실행 시간: 2025-02-20 10:32:50 / 최근 3시간 / 검색어: 반도체 ===
[KBS 뉴스] ‘반도체 기술 유출’ 전직 삼성전자 부장, 1심서 징역 7년 (53분 전)
    Link->https://news.kbs.co.kr/news/view.do?ncd=8181071
[한국경제] ‘반도체 제조 종합 솔루션 기업’으로 거듭난 한화세미텍 (2시간 전)
    Link->https://www.hankyung.com/article/202502207180P
[연합뉴스] [속보] 트럼프 "車·반도체 관세, 한 달내 또는 그보다 일찍 발표" (2시간 전)
    Link->https://www.yna.co.kr/view/AKR20250220027200071
[NATE] 트럼프 "車·반도체·의약품·목재 등의 관세, 한 달내 발표"(종합) (2시간 전)
    Link->https://news.nate.com/view/20250220n05938
[조선일보] 트럼프 “車·반도체 관세, 한달 후 또는 그보다 일찍 발표" (2시간 전)
    Link->https://www.chosun.com/international/us/2025/02/20/VQALRQL5VNDJNNHY6O2XMOYMTI/
[뉴스1] 인텔 6% 이상 급락에도 반도체지수 1.18% 상승(종합) (3시간 전)
    Link->https://www.news1.kr/world/usa-canada/5695569
[글로벌이코노믹] 일본 파워반도체 기업들, 실적 부진 심화...중국발 위기 직면 (3시간 전)
    Link->https://www.g-enews.com/article/Global-Biz/2025/02/202502200647529074fbbec65dfb_1
```
---

# Google 검색 와일드카드 및 연산자 활용방법법

| 검색 연산자 | 기능 | 예제 |
|------------|------------------------------------------------|--------------------------------|
| `*` | 중간에 아무 단어나 포함 | `"삼성 * 반도체"` |
| `""` | 정확한 문구 검색 | `"삼성 반도체"` |
| `intitle:` | 제목에 특정 단어 포함 | `intitle:"삼성 반도체"` |
| `site:` | 특정 웹사이트 내에서 검색 | `site:naver.com "삼성 반도체"` |
| `-` | 특정 단어 제외 | `"삼성 반도체" -TSMC` |
| `OR` | 두 개 이상의 키워드 중 하나 포함 | `삼성 OR SK 반도체` |


---
