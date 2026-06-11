---
layout: post
date: 2026-05-21
title: 11. K-Means 군집화 (K-Means Clustering)
author: Voliti
category_name: python
---

**비지도학습(Unsupervised Learning)**은 정답 타겟 라벨($Y$)이 제공되지 않은 채 데이터 자체의 특성(Feature)과 내부 구조를 파악해 스스로 학습하는 방식임. 대표적인 비지도학습 알고리즘인 **K-Means 군집화(Clustering)**는 데이터를 서로 유사한 성격의 $K$개 그룹(군집)으로 결합하여 묶어주는 통계 기법임.

---

## 1. K-Means 작동 원리

### 1) 군집 수 설정 및 초기화
사용자가 지정한 군집 개수 $K$에 맞춰 임의의 위치에 $K$개의 중심점(Centroid)을 설정함.

### 2) 그룹 할당 및 중심점 업데이트 과정
1. 모든 데이터 포인트는 거리상 가장 가까운 중심점 그룹으로 할당됨.
2. 각 그룹에 소속된 데이터 포인트들의 좌표 평균값을 구해 새로운 중심점 좌표로 업데이트함.
3. 데이터 포인트의 그룹 재할당이 일어나지 않고 중심점이 고정될 때까지 위 과정을 반복함.

---

## 2. 파이썬 실습: 과일 특성 기준 군집화

### 1) 데이터 로드 및 초기 분포
수박, 자두, 참외의 무게와 길이 데이터셋을 불러온 뒤, 임의의 초기 중심점 3개($x_1, y_1 = 2000, 22$, $x_2, y_2 = 200, 2.5$, $x_3, y_3 = 500, 10$)를 설정하여 산점도를 그림.

```python
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
fruits = pd.read_csv('과일3개.csv', encoding='cp949')

# 독립변수 정의 (타겟 없이 특성만 활용)
data = fruits[['무게_g', '길이_cm']]
```

![K-Means 수행 전 데이터 분포 및 초기점]({{site.baseurl}}/assets/images/kmeans_before.png)

### 2) K-Means 군집 모델 정의 및 학습
수동 설정한 초기점 위치를 기반으로 `KMeans` 모델을 정의하고 학습을 시킴.

```python
import numpy as np
from sklearn.cluster import KMeans

x1, y1 = 2000, 22
x2, y2 = 200, 2.5
x3, y3 = 500, 10

# KMeans 객체 정의
kmeans = KMeans(n_clusters=3, init=np.array([(x1, y1), (x2, y2), (x3, y3)]), n_init=1)
kmeans.fit(data)

# 각 데이터별 군집 라벨(0, 1, 2) 저장
data['cluster'] = kmeans.labels_
final_centroid = kmeans.cluster_centers_

# 군집 결과 데이터프레임 출력
print(data)
```

**실행 결과:**
```
    무게_g  길이_cm  cluster
0   2000   30.0        0
1   2500   25.0        0
...
5    100    3.5        1
...
10   500    8.0        2
```
- **Cluster 0**: 수박 군집
- **Cluster 1**: 자두 군집
- **Cluster 2**: 참외 군집

### 3) 학습 완료된 군집 및 최 중심점 시각화
업데이트가 중단된 최종 중심점을 함께 표시하여 시각화함.

```python
plt.scatter(data['무게_g'], data['길이_cm'], c=data['cluster'])
plt.scatter(final_centroid[:,0], final_centroid[:,1], marker='*', color='red', s=200)
plt.show()
```

![K-Means 군집화 완료 후 산점도]({{site.baseurl}}/assets/images/kmeans_after.png)

### 4) 신규 데이터 군집 예측
새롭게 발견된 과일들의 규격 좌표를 넣어 어떤 군집에 해당할지 매칭함.

```python
# [무게 500g, 길이 20cm] 및 [무게 1700g, 길이 15cm] 데이터 예측
print("500g, 20cm 예측 군집:", kmeans.predict([[500, 20]]))
print("1700g, 15cm 예측 군집:", kmeans.predict([[1700, 15]]))
```

**실행 결과:**
```
500g, 20cm 예측 군집: [2]
1700g, 15cm 예측 군집: [0]
```

---

## 3. 이너샤(Inertia)와 엘보우 기법 (Elbow Method)

K-Means 군집 모델의 품질은 각 중심점으로부터 클러스터 내부 샘플들까지의 거리 제곱 합인 **이너샤(Inertia)** 수치로 대변됨. 이너샤 값이 작을수록 오차가 적고 군집화가 잘 구성되었다고 판단함.

### 1) K-Means 이너샤 확인
```python
print("최종 이너샤 오차값:", kmeans.inertia_)
```

**실행 결과:**
```
최종 이너샤 오차값: 610236.128
```

### 2) 엘보우 기법으로 최적의 군집 수($K$) 찾기
군집의 개수($K$)가 늘어날수록 개별 이너샤 오차는 감소하게 됨. 감소율이 완만해지는 변곡점인 **엘보우(Elbow)** 포인트를 찾아내는 방법으로 최적의 군집 수를 결정함.

```python
inertia = []
k_range = range(2, 15)

for i in k_range:
    km = KMeans(n_clusters=i, random_state=42)
    km.fit(data[['무게_g', '길이_cm']])
    inertia.append(km.inertia_)
```

![엘보우 기법을 통한 최적 군집 수 설정]({{site.baseurl}}/assets/images/kmeans_elbow.png)

- **해석**: 이너샤 하강 곡선을 살펴보면 **K=3** 지점부터 오차의 하락 강도가 눈에 띄게 줄어드는 꺾임(Elbow)이 발생함. 따라서 해당 데이터의 합리적인 군집의 수는 3개로 설정하는 것이 통계적으로 바람직함.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
