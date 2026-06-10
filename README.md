# 영화 리뷰 기반 추천 시스템

한국어 영화 리뷰 데이터를 전처리하고, `TF-IDF`와 `Word2Vec`을 활용해 취향이 비슷한 영화를 추천하는 데스크톱 애플리케이션입니다.  
영화 제목을 선택하면 리뷰 유사도가 높은 작품을 추천하고, 키워드를 입력하면 Word2Vec이 의미적으로 가까운 단어를 확장해 관련 영화를 찾아줍니다.

## 주요 기능

- 한국어 리뷰 텍스트 전처리
  - `Okt` 형태소 분석기를 사용해 명사, 동사, 형용사 중심으로 토큰화
  - 불용어 제거 및 리뷰 문장 정제
- 영화별 리뷰 키워드 워드클라우드 시각화
- `TF-IDF` 기반 영화 리뷰 유사도 계산
- `Word2Vec` 기반 키워드 확장 추천
- `PyQt5` GUI로 영화 제목 선택 및 키워드 검색 지원

## 기술 스택

| 영역 | 사용 기술 |
| --- | --- |
| Language | Python 3.12 |
| NLP | KoNLPy, Okt, Gensim Word2Vec |
| ML / Similarity | scikit-learn TF-IDF, cosine similarity |
| Data | pandas, scipy sparse matrix |
| Visualization | wordcloud, matplotlib |
| GUI | PyQt5, Qt Designer UI |

## 프로젝트 구조

```text
.
├── job01_preprocessing.py       # 리뷰 텍스트 전처리
├── job02_word_cloud.py          # 특정 영화 리뷰 워드클라우드 생성
├── job03_TFIDF.py               # TF-IDF 벡터라이저와 행렬 생성
├── job04_recommendation.py      # 콘솔 기반 추천 로직 테스트
├── job05_word2vec.py            # Word2Vec 모델 학습
├── movie_recommendation_app.py  # PyQt5 추천 앱 실행 파일
├── movie_recommendation.ui      # Qt Designer UI 파일
├── malgun.ttf                   # 한글 워드클라우드용 폰트
├── requirements.txt
└── README.md
```

`datasets/`와 `models/`는 대용량 파일이므로 Git 추적에서 제외되어 있습니다. 실행 전 아래 구조로 직접 준비해야 합니다.

```text
datasets/
├── reviews_2017_2022.csv
└── stopwords.csv

models/
├── tfidf.pkl
├── tfidf_movie_review.mtx
└── word2vec_movie_review.model
```

## 데이터 형식

`datasets/reviews_2017_2022.csv`는 최소한 아래 두 컬럼을 포함해야 합니다.

| 컬럼 | 설명 |
| --- | --- |
| `titles` | 영화 제목 |
| `reviews` | 영화 리뷰 텍스트 |

예시:

```csv
titles,reviews
기생충,"연출 배우 이야기 몰입감 ..."
헤어질 결심,"분위기 대사 감정 여운 ..."
```

`datasets/stopwords.csv`는 아래처럼 불용어 컬럼을 사용합니다.

```csv
stopword
영화
정말
너무
```

## 설치 방법

가상환경 사용을 권장합니다.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

KoNLPy의 `Okt`를 사용하므로 Java 실행 환경이 필요할 수 있습니다. 형태소 분석 단계에서 Java 관련 오류가 발생하면 JDK 설치 여부와 `JAVA_HOME` 설정을 확인하세요.

## 실행 순서

### 1. 리뷰 전처리

```bash
python job01_preprocessing.py
```

리뷰를 형태소 단위로 정제하고 불용어를 제거합니다. 학습에 사용할 CSV 파일명은 이후 스크립트에서 읽는 경로와 맞춰주세요.

### 2. TF-IDF 모델 생성

```bash
python job03_TFIDF.py
```

아래 파일이 `models/` 폴더에 생성됩니다.

- `tfidf.pkl`
- `tfidf_movie_review.mtx`

### 3. Word2Vec 모델 생성

```bash
python job05_word2vec.py
```

아래 파일이 `models/` 폴더에 생성됩니다.

- `word2vec_movie_review.model`

### 4. 추천 로직 확인

```bash
python job04_recommendation.py
```

콘솔에서 특정 영화와 키워드 기준 추천 결과를 빠르게 확인할 수 있습니다.

### 5. GUI 앱 실행

```bash
python movie_recommendation_app.py
```

앱에서 영화 제목을 선택하면 리뷰 유사도 기반 추천 목록이 표시됩니다. 키워드를 입력하고 추천 버튼을 누르면 Word2Vec으로 의미가 가까운 단어를 확장해 관련 영화를 추천합니다.

## 추천 방식

### 제목 기반 추천

1. 선택한 영화의 리뷰 벡터를 TF-IDF 행렬에서 조회합니다.
2. 전체 영화 리뷰 벡터와 코사인 유사도를 계산합니다.
3. 가장 유사한 상위 영화를 추천합니다.

### 키워드 기반 추천

1. 입력한 키워드를 Word2Vec 모델에서 검색합니다.
2. 의미적으로 가까운 단어를 가져와 가중 문장을 만듭니다.
3. 해당 문장을 TF-IDF 벡터로 변환합니다.
4. 영화 리뷰 벡터와 비교해 관련도가 높은 영화를 추천합니다.

## 워드클라우드

특정 영화의 리뷰 키워드를 시각화하려면 `job02_word_cloud.py`의 `MOVIE_INDEX` 값을 변경한 뒤 실행합니다.

```bash
python job02_word_cloud.py
```

한글이 깨지지 않도록 프로젝트에 포함된 `malgun.ttf`를 사용합니다.

## 주의사항

- `datasets/`와 `models/`는 `.gitignore`에 포함되어 있으므로 저장소에는 올라가지 않습니다.
- 앱 실행 전 `models/tfidf.pkl`, `models/tfidf_movie_review.mtx`, `models/word2vec_movie_review.model`이 모두 필요합니다.
- 입력 키워드가 Word2Vec vocabulary에 없으면 키워드 기반 추천이 동작하지 않습니다.
- CSV 컬럼명은 코드와 동일하게 `titles`, `reviews`를 사용하는 것을 권장합니다.

## 한 줄 요약

영화 리뷰 속 단어의 분위기와 문맥을 읽어, 내가 고른 영화나 키워드와 결이 비슷한 작품을 찾아주는 한국어 영화 추천 시스템입니다.
