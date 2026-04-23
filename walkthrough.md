# 🚗 모리스 메를로-퐁티 연구 대시보드 워크스루 (Walkthrough)

네, 대시보드 로컬 구동 및 UI/UX 개선 작업이 **모두 완료**되었습니다! 현재 `http://localhost:8501`에서 대시보드가 백그라운드로 실행 중입니다. 사용자가 궁금해하신 대시보드의 주요 구조, 데이터 처리 로직, 그리고 기능 설명을 정리해 드립니다.

---

## 1. 코드 스니펫: 주요 구조 및 데이터 처리 로직

### 1-1. 대시보드 UI 구성 부분 (주요 구조)
Streamlit을 활용하여 총 4개의 탭으로 구성된 직관적인 인터페이스를 만들었습니다. 
```python
# 4. 앱 통합 메인 (Entry Point)
def main():
    st.title("🚗 모리스 메를로-퐁티 연구 대시보드")
    st.caption("한국연구재단(KCI) 데이터를 바탕으로 한 졸업 논문 예비탐색 네비게이션입니다.")
    st.markdown("---")
    
    with st.spinner('문헌 데이터베이스를 불러오고 전처리하는 중입니다...'):
        raw_df = validate_and_load_data()
        df = preprocess_data(raw_df)
    
    # 4개의 탭 레이아웃 생성
    t1, t2, t3, t4 = st.tabs(["📊 Total Insight", "🧭 Concept Map", "👥 People & Journal", "📚 Research Library"])
    
    with t1:
        render_tab1(df) # 막대/선 이중축 그래프 렌더링
    with t2:
        render_tab2(df) # 키워드 빈도 바 차트 및 워드클라우드 렌더링
    with t3:
        render_tab3(df) # 저자 바 차트 및 학술지 파이 차트 렌더링
    with t4:
        render_tab4(df) # 데이터프레임 및 초록 검색 UI 렌더링

if __name__ == "__main__":
    main()
```

### 1-2. 핵심 데이터 처리 로직 (형태소 분석 및 결측치 보정)
원시 KCI 데이터를 로드한 후, 의미 있는 분석을 위해 불용어(Stopwords)를 제외하고 핵심 개념어만 추출하는 정제 과정을 거칩니다.
```python
@st.cache_data(show_spinner=False)
def preprocess_data(df):
    df = df.copy()

    # (1) 결측치 보정 및 타입 변환
    if '발행연도' in df.columns:
        df['발행연도'] = pd.to_numeric(df['발행연도'], errors='coerce')
        df = df.dropna(subset=['발행연도']).astype({'발행연도': int})
    
    if '인용된 총 횟수' in df.columns:
        df['인용된 총 횟수'] = pd.to_numeric(df['인용된 총 횟수'], errors='coerce').fillna(0).astype(int)

    # (2) 저자키워드 불용어 처리 (Stopwords Filtering)
    stopwords = ["연구", "분석", "고찰", "현상학", "메를로", "퐁티", "철학", "메를로퐁티", "의미", "현대", "문제", "대한", "통한", "중심", "이해", "방법론", "사유"]
    
    def extract_keywords(text):
        if pd.isna(text): return []
        words = []
        # 정규식을 통한 한국어 2글자 이상 명사 추출
        for match in re.finditer(r'[가-힣]{2,}', str(text)):
            word = match.group()
            if word not in stopwords:
                words.append(word)
        return words
        
    df['저자키워드_추출'] = df.get('저자키워드', pd.Series([None]*len(df))).apply(extract_keywords)
    return df
```

---

## 2. 기능 설명 및 기대 인사이트

### 📌 어떤 데이터를 시각화했는지?
한국연구재단(KCI)에서 수집된 모리스 메를로-퐁티 관련 **약 600여 건의 학술 논문 메타데이터**를 시각화했습니다. 
- **Tab 1:** 연도별 논문 발행 수(막대) 및 인용된 총 횟수 누적(선)
- **Tab 2:** 저자 키워드 기반 빈도 상위 15개 한국어 개념어 및 워드클라우드
- **Tab 3:** 메를로-퐁티 관련 최다 게재 연구자 순위 Top 10 및 주 게재 학술지 비중
- **Tab 4:** 전체 논문 리스트(발행연도/인용수 기준) 및 초록 텍스트

### 🔎 필터 기능은 무엇인지?
- **정렬 필터링:** `Research Library(Tab 4)`에서 테이블 헤더를 클릭하여 발행연도 최신순, 혹은 인용수가 많은 순서대로 데이터를 재정렬할 수 있습니다.
- **키워드 검색 필터:** 검색창(Text Input)에 특정 논문명이나 저자명을 입력하면 해당되는 논문들만 즉시 필터링되어 화면에 아코디언(Expander) 형태로 요약 정보 및 '초록'을 보여줍니다. 

### 💡 사용자가 어떤 인사이트를 얻길 원하는지?
마치 **'차량의 계기판'**처럼, 졸업 논문을 준비하는 연구자가 학계의 거시적 지형을 한눈에 파악하는 것을 목표로 합니다.
1. **역사적 흐름 (Tab 1):** 특정 시점(예: 2010년대)부터 메를로-퐁티 연구가 급증했는지, 영향력(인용수)의 전성기는 언제였는지 파악.
2. **핵심 담론 도출 (Tab 2):** '살', '지각', '신체'와 같은 철학적 고유 개념어 중 학계에서 가장 많이 다루어진 주제가 무엇인지 즉각 확인하여 논문 주제 선정에 활용.
3. **거장 및 주류 학술지 파악 (Tab 3):** 내가 쓴 논문을 인용하거나 참고해야 할 핵심 연구자(Author)가 누구인지, 그리고 논문을 투고하기 유리한 학회지가 어디인지 타겟팅.
4. **문헌 검토 시간 단축 (Tab 4):** 검색과 정렬을 통해 직접 논문 전체를 읽기 전에 초록만 빠르게 훑어봄으로써 문헌 조사(Literature Review)의 효율성을 극대화.

---

> 이제 대시보드가 구동되었으니 내부적인 기능의 활용이나 시각적으로 수정하고 싶은 부분(비판점)에 대해 자유롭게 담론을 나누어 보면 좋겠습니다!
