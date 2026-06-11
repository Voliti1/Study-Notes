---
layout: post
date: 2026-05-17
title: 07. KNN 분류 (K-Nearest Neighbors)
author: Voliti
category_name: python
---

KNN(K-Nearest Neighbors, K-최근접 이웃)은 가장 간단하고 직관적인 **인스턴스 기반 지도학습(Instance-based Learning)** 알고리즘임. 새로운 데이터가 들어왔을 때, 기존 데이터 중에서 거리상 가장 가까운 $K$개의 이웃을 찾아 그 이웃들의 다수결(Majority Vote)로 새로운 데이터의 클래스를 결정함.

---

## 1. KNN 작동 원리 및 거리 측정

### 1) 작동 단계
1. 분류할 새로운 데이터 포인트와의 거리를 계산함.
2. 거리가 가장 가까운 순서대로 $K$개의 기존 데이터를 선택함.
3. 선택된 $K$개 데이터의 클래스 비율 중 다수를 차지하는 클래스로 새로운 데이터를 분류함.

### 2) 유클리드 거리 (Euclidean Distance)
가장 보편적인 거리 측정법인 유클리드 거리를 기반으로 거리를 계산함. 두 점 $A(x_1, y_1)$와 $B(x_2, y_2)$ 사이의 거리는 다음과 같음.
$$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$

---

## 2. 파이썬 실습: 수박과 참외 분류

### 1) 데이터 로드 및 확인
무게와 길이에 따른 과일(수박, 참외) 종류 데이터셋을 불러옴.

```python
import pandas as pd
import numpy as np

# 데이터 로드
src_data = pd.read_csv('./머신러닝실습용자료/수박과참외.csv', encoding='cp949')
src_data.head()
```

**실행 결과:**
```
     종류    무게    길이
0   수박  2000  30.0
1   수박  2500  25.0
2   수박  1800  20.0
...
13  참외   400   4.5
14  참외   600   8.5
```

### 2) 특성(Feature) 및 타겟(Target) 정의
`numpy.column_stack`을 활용해 독립변수 리스트를 구성하고, 종류를 타겟으로 지정함.

```python
data = np.column_stack((src_data.무게, src_data.길이))
target = src_data.종류
```

### 3) 훈련 및 테스트 데이터셋 분할
```python
from sklearn.model_selection import train_test_split
훈련용_data, 테스트용_data, 훈련용_target, 테스트용_target = train_test_split(
    data, target, test_size=0.25, random_state=40
)
```

### 4) KNN 모델 학습 및 평가 ($K=1$)
```python
from sklearn.neighbors import KNeighborsClassifier

# 가장 가까운 이웃 1개 기준의 모델 생성
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(훈련용_data, 훈련용_target)

print("훈련용 정확도 점수:", knn.score(훈련용_data, 훈련용_target))
print("테스트용 정확도 점수:", knn.score(테스트용_data, 테스트용_target))
```

**실행 결과:**
```
훈련용 정확도 점수: 1.0
테스트용 정확도 점수: 1.0
```

### 5) 신규 데이터 예측 및 데이터 분포 시각화
무게가 `1000g`이고 길이가 `15cm`인 신규 데이터의 종류를 예측함.

```python
print("예측 결과:", knn.predict([[1000, 15]]))
```

**실행 결과:**
```
예측 결과: ['수박']
```

![KNN 데이터 분포 및 예측 포인트]({{site.baseurl}}/assets/images/knn_scatter.png)

---

## 3. 하이퍼파라미터 $K$의 튜닝

$K$가 너무 작으면 ($K=1$) 훈련 데이터의 이상치(Outlier)에 민감하게 작용하여 과대적합(Overfitting)될 확률이 높음. 반대로 $K$가 너무 크면 모델이 너무 단순해져 과소적합(Underfitting)이 발생할 수 있으므로, 적절한 이웃 수($K$) 설정이 필요함.

### 1) 최적의 K 찾기
반복문을 돌려 검증 데이터의 정확도가 높은 최적의 이웃 수를 모니터링함.

```python
k_list = range(1, 12)
accuracies = []

for k in k_list:
    classifier = KNeighborsClassifier(n_neighbors=k)
    classifier.fit(훈련용_data, 훈련용_target)
    accuracies.append(classifier.score(테스트용_data, 테스트용_target))
```

![최적의 이웃 값 찾기 정확도 곡선]({{site.baseurl}}/assets/images/knn_k_accuracy.png)

### 2) 최적의 이웃 수 ($K=3$) 적용 모델 성능
```python
# K=3으로 지정하여 재학습
knn_3 = KNeighborsClassifier(n_neighbors=3)
knn_3.fit(훈련용_data, 훈련용_target)

print("K=3 훈련용 정확도 점수:", knn_3.score(훈련용_data, 훈련용_target))
print("K=3 테스트용 정확도 점수:", knn_3.score(테스트용_data, 테스트용_target))
```

**실행 결과:**
```
K=3 훈련용 정확도 점수: 0.9090909090909091
K=3 테스트용 정확도 점수: 1.0
```
- $K=3$으로 이웃 수를 넓혔을 때 훈련 세트 정확도가 살짝 감소하지만 과적합을 방지하고 더 일반화된 예측 경계를 확보할 수 있음.

---

## 4. 모델 저장 및 외부 데이터 예측 (Model Serialization)

학습 완료된 머신러닝 모델을 파일로 내보내 저장(Dump)하고 필요할 때 다시 불러와서(Load) 재사용하는 방식을 실습함.

### 1) 모델 저장
```python
import joblib

# joblib을 활용하여 학습 완료된 객체를 pkl 파일로 저장
joblib.dump(knn_3, "KNN_model.pkl")
```

### 2) 외부 스크립트에서 모델 로드 및 예측
```python
import joblib

# 저장된 pkl 파일을 다시 불러오기
loaded_model = joblib.load("KNN_model.pkl")

# 신규 참외 데이터(무게 800g, 길이 8cm) 예측
print("불러온 모델의 예측값:", loaded_model.predict([[800, 8]]))
```

**실행 결과:**
```
불러온 모델의 예측값: ['참외']
```

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
