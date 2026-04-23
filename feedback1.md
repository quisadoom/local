# 📊 Merleau-Ponty Research Data Dashboard
> **철학적 현상학과 데이터 시각화의 결합:** KCI 학술 데이터를 기반으로 한 메를로-퐁티 연구 동향 분석 대시보드입니다.

---

## 1. 🎯 프로젝트 개요 (Project Overview)
본 프로젝트는 **메를로-퐁티(Maurice Merleau-Ponty)**와 관련된 국내 연구 문헌 데이터(KCI, 약 870건)를 체계적으로 시각화하여, 연구 흐름을 한눈에 파악하고 졸업논문 작성을 위한 학술적 통찰을 얻는 것을 목적으로 합니다.

* **주요 대상**: 메를로-퐁티 현상학, 신체성, 지각의 현상학 관련 연구 데이터
* **핵심 가치**: 방대한 선행 연구의 메타데이터를 정량적으로 분석하여 연구 공백 및 트렌드 발견
* **개발 철학**: AI 어시스턴트를 적극 활용하는 **'Vibe Coding'**과 **AI Fluency(3A/4D)** 프레임워크 적용

---

## 2. 🛠 기술 스택 (Tech Stack)
| 분류 | 기술 및 도구 |
| :--- | :--- |
| **Language** | Python 3.x |
| **Framework** | Streamlit |
| **Data Analysis** | Pandas, NumPy |
| **Database** | SQLite3, CSV |
| **Environment** | VS Code (Continue), Git/GitHub |
| **Visualization** | Plotly, Matplotlib |

---

## 3. 🏗 데이터 아키텍처 (Data Architecture)
데이터 수집부터 시각화까지의 파이프라인은 다음과 같이 구성됩니다.

1.  **Data Extraction**: KCI에서 870여 건의 논문 데이터를 Excel/CSV 형태로 추출.
2.  **Data Cleaning**: 중복 제거, 연도별 데이터 정규화, 키워드 파싱(Parsing).
3.  **Local Storage**: `C:\dashboard` 환경의 SQLite DB에 적재하여 쿼리 성능 최적화.
4.  **UI/UX Rendering**: Streamlit을 통해 다크 퍼플(#3F0099) 테마 기반의 인터랙티브 UI 구현.

---

## 4. ✨ 핵심 기능 (Key Features)

### 🔍 인터랙티브 필터링 및 검색
* **연도별 슬라이더**: 특정 시기(예: 1990년대 vs 2020년대)의 연구 빈도 비교.
* **키워드 클러스터링**: '신체', '세계-내-존재', '살(Chiasme)' 등 핵심 개념별 연구 분포 확인.
* **저자/학술지 분석**: 메를로-퐁티 담론이 활발한 주요 학술지 및 연구자 매핑.

### 📈 데이터 시각화
* **Time-series Chart**: 연도별 연구 논문 발행 수의 증감 추이 시각화.
* **Topic Distribution**: 연구 분야(철학, 예술학, 교육학 등) 간의 비중 분석.
* **Raw Data Explorer**: 필터링된 전체 논문 리스트를 확인하고 원문 링크로 연결.

---

## 5. 💡 구현 기록 및 통찰 (Development Log)
* **Vibe Coding 적용**: AI를 활용하여 CLI 환경에서 데이터베이스 연결 로직과 Streamlit 레이아웃을 신속하게 구현.
* **3A/4D 프레임워크**:
    * **Automation**: 반복적인 데이터 정제 프로세스 자동화.
    * **Augmentation**: 연구자의 직관을 넘어서는 데이터 중심의 트렌드 발견.
    * **Agency**: 대시보드를 통한 연구 데이터 통제권 확보.
* **디자인 가이드**: 철학적 무게감을 전달하기 위해 `#3F0099` (Dark Purple) 테마와 카드형 UI 레이아웃 채택.

---

## 6. 🚀 향후 계획 (Future Roadmap)
* [ ] 논문 초록(Abstract) 텍스트 마이닝을 통한 워드클라우드 기능 고도화.
* [ ] 주요 철학자 간 인용 네트워크 그래프 구현.
* [ ] 졸업논문 서론 초안 작성을 위한 데이터 기반 리포트 자동 생성 모듈 추가.

---

## 🖥 실행 방법 (Usage)
```bash
# 관련 라이브러리 설치
pip install streamlit pandas matplotlib plotly

# 대시보드 실행
streamlit run app.py