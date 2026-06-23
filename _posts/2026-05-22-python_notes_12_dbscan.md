---
layout: post
date: 2026-05-22
title: 12. DBSCAN 군집화 (DBSCAN Clustering)
author: Voliti
category_name: python
subcategory: ai
---

K-Means 군집 분석은 학습 속도가 빠르고 직관적이지만 **구형(Spherical) 형태의 단순 군집** 분포만 탐색할 수 있어 초승달 형태나 도넛 형태 등 기하학적 형태의 비선형적 군집 데이터를 해결하지 못하고 잘못 분할하는 한계가 있음. 이러한 한계를 보완하기 위해 밀도 분포(Density)를 기반으로 공간을 그룹화하는 **DBSCAN(Density-Based Spatial Clustering of Applications with Noise)** 알고리즘을 도입함.

---

## 1. DBSCAN의 핵심 동작 원리 및 파라미터

### 1) 주요 하이퍼파라미터
- **`eps` (epsilon, 입실론)**: 데이터를 중심으로 군집을 판단할 주변 반경(거리 제한)을 지정함.
- **`min_samples`**: 특정 데이터의 입실론 반경 내에 군집의 일원으로 취급할 최소 데이터 포인트의 개수를 지정함.

### 2) 데이터 포인트 분류
- **핵심 포인트 (Core Point)**: 입실론 반경 내에 자기 자신을 포함하여 최소 `min_samples` 수 이상의 데이터가 포함되어 있는 포인트를 의미함.
- **경계 포인트 (Border Point)**: 핵심 포인트의 반경 내에 인접해 있지만, 자체 반경 내에는 최소 샘플 수 기준을 만족하지 못하는 포인트를 의미함.
- **잡음/아웃라이어 포인트 (Noise Point)**: 핵심 포인트와 경계 포인트 둘 다 해당하지 않는 외딴 데이터를 의미하며, 최종 라벨링 시 `-1`로 격리 분류함.

---

## 2. 실습 1: 초승달(Moons) 데이터 군집 비교

비선형적 초승달 분포를 가진 모의 데이터셋을 활용해 K-Means와 DBSCAN의 성능을 시각적으로 비교해 봄.

```python
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt

# 2차원 초승달 데이터 400개 생성
X, y = make_moons(n_samples=400, noise=0.1, random_state=10)
```

### 1) K-Means 군집 시도
```python
from sklearn.cluster import KMeans

# 2개의 군집으로 시도
km = KMeans(n_clusters=2, random_state=10)
y_km = km.fit_predict(X)
```

![K-Means moons 실패 결과]({{site.baseurl}}/assets/images/dbscan_moons_kmeans.png)
- **K-Means 결과 분석**: 기하학적 형태를 인지하지 못하고 단순히 반반으로 직선 분할하여 잘못 구분하는 한계를 보임.

### 2) DBSCAN 군집 시도
```python
from sklearn.cluster import DBSCAN

# 반경 0.2, 최소샘플 15 설정
db = DBSCAN(eps=0.2, min_samples=15, metric='euclidean')
y_db = db.fit_predict(X)
```

![DBSCAN moons 성공 결과]({{site.baseurl}}/assets/images/dbscan_moons_dbscan.png)
- **DBSCAN 결과 분석**: 밀도 기반 연결 방식을 통해 2개의 독립적인 초승달 곡선 형태를 정확하게 인식하여 분류해 냄.

---

## 3. 실습 2: 동심원(Circles) 데이터 군집 비교

이번에는 하나의 원 안에 또 다른 원이 감싸고 있는 동심원 구조를 띠는 데이터셋을 분류함.

```python
from sklearn.datasets import make_circles
import pandas as pd
import numpy as np

# 동심원 구조 1000개 데이터셋 생성
X, y = make_circles(n_samples=1000, shuffle=True, noise=0.05, random_state=0, factor=0.5)
```

### 1) K-Means 결과
```python
kmeans = KMeans(n_clusters=2, max_iter=1000, random_state=0)
y_km_circle = kmeans.fit_predict(X)
```

![K-Means circles 실패 결과]({{site.baseurl}}/assets/images/dbscan_circles_kmeans.png)
- **결과**: 내부 원과 외부 원을 구별하지 못하고 위아래 반원 형태로 잘라서 구분함.

### 2) DBSCAN 결과
```python
dbscan = DBSCAN(eps=0.2, min_samples=20, metric='euclidean')
y_db_circle = dbscan.fit_predict(X)
```

![DBSCAN circles 성공 결과]({{site.baseurl}}/assets/images/dbscan_circles_dbscan.png)
- **결과**: 내부 중심 밀집 구역과 외부 고리 밀집 구역을 독립된 밀도로 인지하여 두 개의 원 형태로 완벽히 분류 완료함.

---

## 4. K-Means vs DBSCAN 비교 요약

| 구분 | K-Means 군집화 | DBSCAN 군집화 |
| :--- | :--- | :--- |
| **군집 개수 ($K$)** | **사전 지정 필수** | **자동 결정** (밀도 기준) |
| **군집 탐색 형태** | 원형 / 구형 분포 중심 | 임의의 밀집된 형태 (곡선 등) |
| **이상치 처리** | 모든 샘플을 억지로 포함시킴 | 이상치(Noise) 식별 및 격리 (`-1`) |
| **주요 파라미터** | 군집 수 ($K$) | 반경(`eps`), 최소 이웃 수(`min_samples`) |
| **동작 속도** | 비교적 빠름 | 데이터량이 많아질수록 다소 느려짐 |

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
