# FinPin_Deploy
spaCy(ko_core_news_sm) 모델을 Streamlit Cloud 환경에서 적용하려 했으나, 모델을 찾을 수 없다는 에러 발생 ➡️ 한국어 BERT 모델과 영어 BERT 모델을 각각 사용하여 키워드를 감지하는 방식으로 알고리즘 변경
![image](https://github.com/user-attachments/assets/0509aff3-49a7-43db-b81c-d7aec34fbe87)


<br>
<br>

## 접속 사이트
https://finpindeploy.streamlit.app/



<br>
<br>

### Before
- spaCy의 한 종류인 한국어 특화 모델인 ko_core_news_sm 사용
- 특정 키워드 리스트는 한국어와 영어를 혼재하여 제작
- 사용자 입력에서 키워드 추출
- 날짜 추출(오늘 날짜 감지)
```python
# spaCy 모델 로드 (한국어)
nlp = spacy.load("ko_core_news_sm")

# 특정 키워드 리스트
predefined_keywords = [
    'Tesla', 'Bitcoin', 'Stock', '경제', '금융', '주식', '테슬라', '비트코인', 
    '금리', '채권', '주식시장', '증권', '주식거래', 'ETF', '포트폴리오', '펀드', 
    '주식투자', '가상화폐', '크립토', '블록체인', '상장', '코스피', '코스닥', 
    '상장폐지', '상장주식', '배당', '주식배당', '시가총액', '이자율', '자산', 
    '자산운용', '리스크관리', '채권시장', '헤지펀드', '투자전략', '경제지표', 
    '물가', '소비자물가', '환율', '금융위기', '금융정책', '금융시스템', '국채', 
    '지수', '상승률', '하락률', '증시', '매수', '매도', '자산관리', '고배당주', 
    '금융상품', '부동산', '모기지', '대출', '채권금리', '금융기관', '거래소', 
    '리보금리', '금융규제', 'FOMC', 'IMF', 'OECD', 'GDP', '실업률', '인플레이션', 
    '유동성', '마진', '헤지', '옵션', '선물', '주식분석', '기업분석', '매출', '순이익', 
    '영업이익', '비즈니스모델', '가치투자', '성장투자', '워런버핏', '테크주', '그로쓰', 
    '인덱스펀드', '투자자', '주요지표', '저금리', '금융사기', '핀테크', '모바일뱅킹', 
    '디지털자산', '핀테크기업', '금융기술', '블록체인기술', '디지털화폐', '리브라', 
    '스테이블코인', '대체투자', '경기지표', '증권사', '금융컨설팅', '고정금리', 
    '변동금리', '국제금융', '금융분석', '경제위기', '경제성장', '고용지표', '상장기업', 
    '투자기회', '정책금리', '기준금리', '금융거래', '가치주', '성장주', '신용카드', 
    '해외주식', '자본시장', '중앙은행', '금융업계', '회계기준', '기업회계', '회계사'
]


# 사용자 입력에서 키워드를 추출하는 함수
def extract_keyword(text):
    """사용자 입력에서 키워드를 추출합니다."""
    doc = nlp(text)
    
    # PhraseMatcher를 사용하여 미리 정의된 키워드를 문장에서 찾기
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(keyword) for keyword in predefined_keywords]
    matcher.add("PredefinedKeywords", patterns)

    matches = matcher(doc)
    matched_keywords = [doc[start:end].text for _, start, end in matches]

    # 키워드가 있으면 추출하고, 없으면 None 반환
    if matched_keywords:
        return matched_keywords[0]  # 첫번째 키워드만 반환
    else:
        return None


# 날짜 추출 함수
def extract_date(text):
    """
    입력된 텍스트에서 날짜를 추출합니다.
    - "YYYY년 MM월 DD일", "MM월 DD일", "DD일" 등의 다양한 형식 지원
    - 형식이 없으면 None 반환
    """
    today = datetime.today()
    
    # 정규 표현식 패턴
    patterns = [
        (r"(\d{4})년 (\d{1,2})월 (\d{1,2})일", "%Y년 %m월 %d일"),  # YYYY년 MM월 DD일
        (r"(\d{1,2})월 (\d{1,2})일", "%m월 %d일"),                # MM월 DD일
        (r"(\d{1,2})일", "%d일")                                  # DD일
    ]
    
    for pattern, date_format in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                if date_format == "%d일":  # 날짜만 주어진 경우
                    day = int(match.group(1))
                    return today.replace(day=day)  # 이번 달의 해당 날짜 반환
                elif date_format == "%m월 %d일":  # 월과 날짜만 주어진 경우
                    month, day = map(int, match.groups())
                    return today.replace(month=month, day=day)
                else:  # YYYY년 MM월 DD일 형식
                    return datetime.strptime(match.group(), date_format)
            except ValueError:
                # 유효하지 않은 날짜일 경우 무시
                continue
    
    return None
```

<br>


### After
- spaCy의 한 종류인 한국어 특화 모델인 ko_core_news_sm 사용
- 특정 키워드 리스트를 한국어와 영어로 "나누어" 제작
- 한국어일 경우 한국어 리스트로, 영어일 경우 영어 리스트로 나누어 조건문이 실행됨
- 또한, 한국어와 영어의 혼재가 있을 경우도 나누어 실행
- 날짜 추출(오늘 날짜 감지) -> "오늘"이라는 단어도 자동 감지할 수 있도록 코드 추가
```python
# 한국어 모델 로드
ko_tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
ko_model = BertForTokenClassification.from_pretrained('monologg/kobert')
ko_nlp = pipeline('ner', model=ko_model, tokenizer=ko_tokenizer)

# 영어 모델 로드
en_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
en_model = BertForTokenClassification.from_pretrained('bert-base-uncased')
en_nlp = pipeline('ner', model=en_model, tokenizer=en_tokenizer)

# 한국어 키워드 추출 함수
def extract_korean_keywords(text):
    # 한국어 키워드 추출 로직을 여기에 작성
    korean_keywords = []
    # 예시: 한국어 키워드 목록에 맞춰 추가
    korean_keyword_list = [
        '경제', '금융', '주식', '테슬라', '비트코인', '금리', '채권', '주식시장', '증권', '주식거래',
        '포트폴리오', '펀드', '주식투자', '가상화폐', '크립토', '블록체인', '상장', '코스피', '코스닥',
        '상장폐지', '상장주식', '배당', '주식배당', '시가총액', '이자율', '자산', '자산운용', '리스크관리',
        '채권시장', '헤지펀드', '투자전략', '경제지표', '물가', '소비자물가', '환율', '금융위기', '금융정책',
        '금융시스템', '국채', '지수', '상승률', '하락률', '증시', '매수', '매도', '자산관리', '고배당주’, ‘금융상품',
        '부동산', '모기지', '대출', '채권금리', '금융기관', '거래소', '리보금리', '금융규제', '실업률', '인플레이션',
        '유동성', '마진', '헤지', '옵션', '선물', '주식분석', '기업분석', '매출', '순이익', '영업이익', '비즈니스모델',
        '가치투자', '성장투자', '워런버핏', '테크주', '그로쓰', '인덱스펀드', '투자자', '주요지표', '저금리', '금융사기',
        '핀테크', '모바일뱅킹', '디지털자산', '핀테크기업', '금융기술', '블록체인기술', '디지털화폐', '리브라', 
        '스테이블코인', '대체투자', '경기지표', '증권사', '금융컨설팅', '고정금리', '변동금리', '국제금융', '금융분석',
        '경제위기', '경제성장', '고용지표', '상장기업', '투자기회', '정책금리', '기준금리', '금융거래', '가치주', '성장주',
        '신용카드', '해외주식', '자본시장', '중앙은행', '금융업계', '회계기준', '기업회계', '회계사'
    ]
    for keyword in korean_keyword_list:
        if keyword in text:
            korean_keywords.append(keyword)
    return korean_keywords

# 영어 키워드 추출 함수
def extract_english_keywords(text):
    # 영어 키워드 추출 로직을 여기에 작성
    english_keywords = []
    # 예시: 영어 키워드 목록에 맞춰 추가
    english_keyword_list = ['Tesla', 'Bitcoin', 'Stock', 'Tesla', 'Bitcoin', 'Stock', 'ETF', 'FOMC', 'IMF', 'OECD', 'GDP']
    for keyword in english_keyword_list:
        if keyword.lower() in text.lower():
            english_keywords.append(keyword)
    return english_keywords

# 혼합된 언어에서 키워드 추출
def extract_keywords(text):
    korean_keywords = extract_korean_keywords(text)
    english_keywords = extract_english_keywords(text)
    
    # 중복된 키워드 제거 후 합침
    return list(set(korean_keywords + english_keywords))


# 날짜 추출 함수
def extract_date(text):
    if not isinstance(text, str):
        return None

    today = datetime.today()

    # "오늘" 처리
    if "오늘" in text:
        return today

    # 정규 표현식 패턴 (공백 처리 개선)
    patterns = [
        (r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", "%Y년 %m월 %d일"),  # YYYY년 MM월 DD일
        (r"(\d{1,2})월\s*(\d{1,2})일", "%m월 %d일"),                # MM월 DD일
        (r"(\d{1,2})일", "%d일")                                  # DD일
    ]
    
    for pattern, date_format in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                if date_format == "%d일":  # 날짜만 주어진 경우
                    day = int(match.group(1))
                    return today.replace(day=day)  # 이번 달의 해당 날짜 반환
                elif date_format == "%m월 %d일":  # 월과 날짜만 주어진 경우
                    month, day = map(int, match.groups())
                    return today.replace(month=month, day=day)
                else:  # YYYY년 MM월 DD일 형식
                    return datetime.strptime(match.group(), date_format)
            except ValueError:
                continue
    
    return None

```


<br>
<br>

## 추후 작업
- 코드 리팩토링 필수!
- 프롬프트 템플릿 적용
- 페르소나 시나리오 빌드업
- 사용자 친화적 서비스로 방향성 고려

<br>
<br>

## 현재 문제 상황(25/01/16 am.12:20)
- 새로운 답변 제공 시, 이전 답변의 HTML 코드 설정이 그대로 노출되고 있음.
- ⚙️ 새로운 질문 후 답변 제공 시점에 그 이전의 답변을 삭제하는 방향으로 수정중
