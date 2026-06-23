---
layout: post
date: 2026-06-05
title: 18. 텍스트 마이닝 및 연관 규칙 분석 (WordCloud & Apriori)
author: Voliti
category_name: python
subcategory: bigdata
---

## 1. KoNLPy 형태소 분석 및 워드클라우드 (WordCloud)

비정형 자연어 텍스트 데이터에서 유의미한 명사 키워드를 추출하여 빈도수에 맞추어 크기별로 시각화하는 과정입니다.

### 1) 분석 순서 및 라이브러리
* **KoNLPy**: 한국어 형태소 분석 라이브러리로, 명사 추출(`Okt.nouns()`)을 수행합니다.
* **WordCloud**: 텍스트 키워드 뭉치를 입력받아 빈도수에 적합한 구형 레이아웃 텍스트 맵을 구축합니다. (반드시 사전 형태로 단어와 빈도수가 매칭된 자료구조가 필요합니다.)

---

## 2. 장바구니 연관 규칙 분석 (Apriori)

고객들의 수많은 거래 내역 속에서 "상품 A와 상품 B가 함께 팔릴 유의미한 패턴이 존재하는가?"를 수학적으로 분석하는 대표적인 무감독 학습(Unsupervised Learning) 기법입니다.

### 1) 세 가지 핵심 평가지표
* **지지도 (Support)**: 전체 전체 거래 중 상품 $X$와 $Y$를 동시에 구매한 거래의 확률적 비율입니다.
  * $Support(X \rightarrow Y) = P(X \cap Y)$
* **신뢰도 (Confidence)**: 상품 $X$를 구매한 고객 중 상품 $Y$도 연속해서 같이 장바구니에 담은 조건부 확률의 개념입니다.
  * $Confidence(X \rightarrow Y) = \frac{P(X \cap Y)}{P(X)}$
* **향상도 (Lift)**: $X$를 산 것이 $Y$를 산 것과 무관한 일반적인 $Y$ 구매율에 비해 구매 성공 확률을 얼마나 높여주었는지의 가중 계수입니다.
  * $Lift(X \rightarrow Y) = \frac{Confidence(X \rightarrow Y)}{P(Y)}$
  * **$Lift > 1$**: 강한 양의 연관성 (A를 사면 B를 살 확률이 평소보다 높아짐)
  * **$Lift = 1$**: 독립적인 관계 (아무런 연관이 없음)
  * **$Lift < 1$**: 음의 연관성 (A를 사면 오히려 B를 살 확률이 감소함)

### 2) Apriori 실습 파이프라인
```python
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# 중복 거래 내역 소거 후 트랜잭션별 리스트 구성
temp = df[['Transaction', 'Item']].drop_duplicates()
temp = temp.groupby('Transaction')['Item'].apply(list).to_list()

# 트랜잭션 매트릭스 인코딩 (One-Hot boolean Matrix 변환)
te = TransactionEncoder()
trans_matrix = te.fit(temp).transform(temp)
basket = pd.DataFrame(trans_matrix, columns=te.columns_)

# 최소 지지도 0.01 이상인 빈발 항목셋 탐색
freq_item = apriori(df=basket, min_support=0.01, use_colnames=True)

# 향상도(lift)가 최소 1 이상인 유의미한 연관 규칙 도출 및 신뢰도 내림차순 정렬
rules = association_rules(df=freq_item, metric='lift', min_threshold=1)
rules.sort_values('confidence', ascending=False, inplace=True)
```
