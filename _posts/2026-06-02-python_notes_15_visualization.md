---
layout: post
date: 2026-06-02
title: 15. 단일/다중변수 데이터 탐색 및 Matplotlib (Data Exploration)
author: Voliti
category_name: python
subcategory: bigdata
---

## 1. 단일변수 범주형 데이터 탐색

범주형 데이터는 질적 자료로 숫자가 지닌 크기가 의미를 갖지 않으며 그룹을 구별할 때 주로 쓰입니다.

### 1) 도수분포 계산
* **`value_counts()`**: 각 범주별 출현 횟수(도수)를 내림차순 또는 오름차순으로 정리하여 시리즈로 반환합니다.

### 2) Matplotlib를 이용한 시각화
```python
import matplotlib.pyplot as plt

# 2x2 그리드로 다중 그래프 영역(Subplot) 구성
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
plt.suptitle('선호 계절 분석 도표') // 전체 대제목

# 세로 막대그래프 (rot = 0: x축 레이블 회전 없음)
fd.plot.bar(xlabel='Season', ylabel='Freq', rot=0, ax=axes[0, 0])

# 가로 막대그래프
fd.plot.barh(xlabel='Freq', ylabel='Season', rot=0, ax=axes[0, 1])

# 원 그래프 (autopct: 백분율 소수점 포맷 지정)
fd.plot.pie(ylabel='', autopct='%1.0f%%', ax=axes[1, 0])

plt.subplots_adjust(left=0.2) // 여백조정
```

---

## 2. 단일변수 연속형 데이터 탐색

연속형 데이터는 양적 자료로 평균과 사분위수 등의 요약 통계량이 중요한 분석 포인트가 됩니다.

### 1) 주요 요약 통계량
* **`mean()`**: 데이터의 산술 평균값을 구합니다. (극단치나 아웃라이어에 큰 왜곡을 겪으므로 평균에만 전적으로 의존해선 안 됩니다.)
* **`median()`**: 크기 순서로 정렬했을 때 가장 가운데에 위치하는 중앙값을 도출합니다.
* **`quantile()`**: 사분위수를 구합니다. (예: `quantile(0.25)`는 하위 25% 지점)
* **`var()` & `std()`**: 데이터가 평균을 중심으로 흩어진 정도를 나타내는 분산과 표준편차입니다.
* **`describe()`**: 기초적인 개수, 평균, 편차, 사분위수 등을 단번에 정리하여 리포트합니다.

### 2) 히스토그램 및 상자그림
* **히스토그램 (`hist(bins=N)`)**: 연속적인 데이터를 구간별(bins)로 묶어 밀도나 개수를 기둥 크기로 표현합니다.
* **상자그림 (`boxplot()`)**: 중앙값, 사분위수, 최댓값, 최솟값을 상자와 선으로 요약 표시하며 상한/하한 울타리를 넘는 극단 아웃라이어 점을 점으로 나타냅니다.

---

## 3. 다중변수 데이터 탐색 및 상관분석

두 개 이상의 변수가 지니는 연관성 및 선형적 규칙성을 분석하는 영역입니다.

### 1) 산점도 (Scatter Plot)
* **`plot.scatter(x, y, s, c, marker)`**: 2차원 평면 위에 점으로 분포를 찍어 시각화합니다. (`s`는 점의 크기, `c`는 컬러)
* **`scatter_matrix(df[vars])`**: 정의된 여러 변수들 간의 산점도를 정사각 행렬 구조로 일괄 매핑하여 상호 상관성을 한눈에 보게 돕습니다.

### 2) 피어슨 상관계수 ($r$)
상관분석은 두 연속형 변수 사이의 선형성 강도를 나타내는 척도입니다.
* 상관계수 $r$은 $-1$ 이상 $1$ 이하의 범위를 가집니다.
* $r > 0$이면 양의 선형 관계, $r < 0$이면 음의 선형 관계를 나타내며 절댓값이 1에 가까울수록 선형 관계가 강함을 의미합니다.

```python
# 피어슨 상관계수 도출 (person은 피어슨(Default), 외에도 kendall, spearman 제공)
correlation_matrix = df.corr(method='pearson')

# polyfit을 이용한 1차 회귀방정식의 기울기(m)와 y절편(b) 계산
m, b = np.polyfit(x, y, 1)
```
