---
layout: post
date: 2026-05-16
title: 06. 로지스틱 회귀분석 (Logistic Regression)
author: Voliti
category_name: python
---

로지스틱 회귀분석(Logistic Regression)은 이름은 회귀이지만 실제로는 **분류(Classification)** 알고리즘에 속함. 선형 회귀와 달리 종속변수가 범주형(예: 합격/불합격, 스팸/정상 등)일 때 사용하며, 출력값을 0과 1 사이의 확률값으로 변환하여 분류를 수행함.

---

## 1. 수학적 모델 및 개념

### 1) 시그모이드 함수 (Sigmoid Function)
이진 분류(Binary Classification)에서 선형 회귀 식의 출력값($z = \beta_0 + \beta_1X$)을 0과 1 사이의 확률값($p$)으로 변환하기 위해 시그모이드 함수를 적용함.
$$p = \sigma(z) = \frac{1}{1 + e^{-z}}$$

- $z$가 무한대로 커지면 $p$는 1에 수렴하고, $z$가 무한대로 작아지면 $p$는 0에 수렴함.
- 확률값 $p$가 0.5 이상이면 양성 클래스(1), 0.5 미만이면 음성 클래스(0)로 예측함.

### 2) 소프트맥스 함수 (Softmax Function)
다중 분류(Multiclass Classification)에서는 각 클래스에 대한 예측 강도를 모두 더했을 때 총합이 1이 되도록 정규화하는 소프트맥스 함수를 사용함.
$$p_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$

---

## 2. 파이썬 실습 1: 이진 분류 (합격/불합격 예측)

### 1) 데이터 로드 및 분리
공부시간에 따른 합격 여부가 기록된 데이터를 로드하여 분석을 준비함.

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# 데이터 로드
study = pd.read_csv('./머신러닝실습용자료/공부시간과시험합격.csv', encoding='cp949')

# 독립변수와 종속변수 설정
data = study['공부시간'].to_numpy()
target = study['합격여부'].to_numpy()

# 훈련용/테스트용 데이터 분리
훈련용_data, 테스트용_data, 훈련용_target, 테스트용_target = train_test_split(
    data, target, test_size=0.2, random_state=40
)
```

### 2) 모델 학습 및 정확도 확인
1차원 배열 데이터를 2차원으로 Reshape한 뒤 `LogisticRegression` 모델로 학습을 수행함.

```python
from sklearn.linear_model import LogisticRegression

# 2차원 배열로 변형
훈련용_data = 훈련용_data.reshape(-1, 1)
테스트용_data = 테스트용_data.reshape(-1, 1)

# 모델 생성 및 학습
lr = LogisticRegression()
lr.fit(훈련용_data, 훈련용_target)

# 정확도 성능 측정
print("테스트용 정확도 점수:", lr.score(테스트용_data, 테스트용_target))
```

**실행 결과:**
```
테스트용 정확도 점수: 0.8
```

### 3) 합격 확률 출력
테스트 데이터의 각 샘플이 각 클래스(불합격, 합격)에 속할 확률을 확인해 봄.

```python
import numpy as np
# 소수점 3자리까지 반올림하여 예측 확률 출력
print(np.round(lr.predict_proba(테스트용_data), 3))
```

**실행 결과:**
```
[[0.668 0.332]
 [0.984 0.016]
 [0.546 0.454]
 [0.849 0.151]
 [0.461 0.539]]
```
- 첫 번째 열은 **불합격 확률**, 두 번째 열은 **합격 확률**을 나타냄.
- 마지막 샘플은 합격 확률이 `0.539`로 0.5 이상이므로 최종 '합격'으로 예측됨.

---

## 3. 파이썬 실습 2: 다중 분류 (과일 종류 분류)

독립변수가 여러 개이고 종속변수의 범주가 3개 이상인 다중 분류 과제를 수행함. 특성의 스케일 차이를 맞추기 위해 **표준화 전처리(StandardScaler)**를 함께 진행함.

### 1) 데이터 로드 및 전처리
```python
# 과일/채소 상세 스펙 데이터 로드
fruit_2 = pd.read_csv('./머신러닝실습용자료/과일채소목록_2.csv', encoding='cp949')

# 특성(무게, 길이, 당도) 및 타겟(종류) 정의
data = fruit_2[['무게_g', '길이_cm', '당도']]
target = fruit_2["종류"]

# 데이터 분리
훈련용_data, 테스트용_data, 훈련용_target, 테스트용_target = train_test_split(
    data, target, test_size=0.2, random_state=40
)
```

### 2) 데이터 표준화 (Standardization)
스케일 차이가 큰 특성(무게_g는 수천 단위, 당도는 10 내외)들을 고르게 조정하여 학습 속도와 정확도를 보장함.

```python
from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(훈련용_data)

표준화_훈련용_data = ss.transform(훈련용_data)
표준화_테스트용_data = ss.transform(테스트용_data)
```

### 3) 다중 로지스틱 회귀 모델 학습 및 결과 확인
```python
# 모델 학습
lr_multi = LogisticRegression()
lr_multi.fit(표준화_훈련용_data, 훈련용_target)

# 테스트 데이터 예측값 출력
print("예측 결과:", lr_multi.predict(표준화_테스트용_data))

# 예측 정확도 평가
print("테스트용 정확도 점수:", lr_multi.score(표준화_테스트용_data, 테스트용_target))
```

**실행 결과:**
```
예측 결과: ['자두' '옥수수' '참외' '자두' '참외' '거봉포도' '수박' '거봉포도' '수박' '거봉포도']
테스트용 정확도 점수: 1.0
```

- 특성 표준화 전처리를 적용한 다중 로지스틱 회귀모델의 테스트 세트 정확도는 **1.0(100%)**을 달성함.
- `predict_proba()`를 통해 확인하면 소프트맥스 함수에 의해 계산된 각 클래스(거봉포도, 수박, 옥수수, 자두, 참외)별 5개 확률값 중 가장 높은 값의 클래스로 정상 분류됨을 확인할 수 있음.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
