---
layout: post
date: 2026-06-03
title: 16. 데이터 전처리 기법 (Data Preprocessing)
author: Voliti
category_name: python
subcategory: bigdata
---

## 1. 결측치(Missing Value)의 확인 및 정제

데이터 수집 단계에서 데이터가 비어 있는 결측치(`NaN`, `None`)를 다루는 방식입니다.

### 1) 기본 결측치 인지 API
* **`isna().sum()`**: 각 컬럼별 결측치 개수를 파악합니다.
* **`notna().sum()`**: 결측치가 아닌 유효 데이터의 개수를 집계합니다.
* **`dropna()`**: 결측치가 포함된 레코드를 삭제합니다.

### 2) KNNImputer와 MinMaxScaler를 이용한 결측치 추정
결측치를 억지로 지우는 대신 기계학습 기반 알고리즘인 **KNN(K-Nearest Neighbors)**을 활용해 주변 유사 이웃들의 평균값으로 자연스럽게 결측치를 채울 수 있습니다.
* **MinMaxScaler**: KNN은 물리적인 '거리'를 연산 기준으로 삼으므로, 단위 숫자가 큰 피처가 거리 연산을 왜곡하는 현상을 방지하고자 전처리 전에 모든 값을 `0`과 `1` 사이 범위로 정규화시킵니다.
* **KNNImputer**: 결측치를 가진 대상과 가장 가까운 $K$개의 이웃 점을 검색하여 이웃들의 평균으로 빈칸을 채웁니다.

```python
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

# 1. 스케일러 정의 및 fit_transform 수행
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df_miss)

# 2. KNNImputer 정의 및 결측치 추정 수행
imputer = KNNImputer(n_neighbors=5)
df_scaled_filled = imputer.fit_transform(df_scaled)

# 3. 데이터 복원을 위해 inverse_transform 수행
df_filled = scaler.inverse_transform(df_scaled_filled)
```

---

## 2. 특이값(Outlier)의 탐색 및 필터링

정상적인 확률적 분포 범위를 완전히 이탈한 특이값(이상치)을 필터링하는 검증 모델입니다.

### 1) Z-Score (표준점수) 기준
데이터가 평균으로부터 표준편차의 몇 배만큼 떨어져 있는지를 보여주는 지표입니다.
* 공식: $Z = \frac{X - \mu}{\sigma}$
* **판단 규칙**: 일반적으로 $Z$-Score의 절댓값이 **2 이상**인 영역을 극단 이상치로 판단하여 슬라이싱 제외합니다.

```python
import numpy as np
from scipy import stats

z = np.abs(stats.zscore(df_data))
clean_data = df_data[z <= 2] // Z-score가 2 이내인 데이터만 보존
```

### 2) IQR (Interquartile Range, 사분범위) 기준
상자그림(Boxplot)의 기본 통계 연산 방식을 적용하는 보편적 룰입니다.
* **IQR**: $Q3(75\%) - Q1(25\%)$
* **상한선(Upper fence)**: $Q3 + (IQR \times 1.5)$
* **하한선(Lower fence)**: $Q1 - (IQR \times 1.5)$
* 상한을 넘거나 하한 미만인 모든 데이터 포인트를 아웃라이어로 간주하여 제외합니다.

---

## 3. 정렬, 순위 및 표본 샘플링

### 1) 정렬과 순위
* **`sort_values(by, ascending)`**: 지정 열을 기준으로 레코드를 정렬합니다. 결측치의 배치 옵션(`na_position`)도 정할 수 있습니다.
* **`rank(pct)`**: 데이터의 순위(석차)를 구합니다. `pct=True` 옵션을 걸어주면 순위를 백분율 비율(0~1)로 표준화합니다.

### 2) 표본 추출 (Sampling)
* **임의 샘플링**: 모집단 전체에서 무작위로 $N$개를 샘플링합니다. (`sample(n=20)`)
* **층화 샘플링(Stratified Sampling)**: 분석하려는 카테고리가 여러 개인 경우 각 그룹별 비율을 균등하게 지키며 골고루 데이터를 샘플링해 오기 위해 `groupby` 연산과 함께 적용합니다.
* **`random_state`**: 난수 생성 알고리즘의 시드값을 고정하여, 추후 동일한 코드를 다시 돌렸을 때도 완벽히 같은 표본이 재현되도록 보장하는 통제용 속성입니다.

```python
# 각 카테고리(Species)별로 20%의 데이터를 균일하게 추출 (재현용 시드 고정)
stratified_sample = df.groupby('Species').apply(
    lambda x: x.sample(frac=0.2, random_state=123)
)
```
