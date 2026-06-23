---
layout: post
date: 2026-06-06
title: 19. 가설 검정 및 통계 분석 (Hypothesis Testing)
author: Voliti
category_name: python
subcategory: bigdata
---

## 1. 통계적 가설 검정 개요 및 절차

수집된 표본(Sample) 데이터를 바탕으로 모집단(Population)에 대한 판단을 통계적 유의성으로 검증하는 절차입니다.

### 1) 가설의 설정
* **귀무가설 ($H_0$)**: 아무런 차이나 효과가 없다는 기본 주장(기각하고자 하는 원래 상태)입니다.
* **대립가설 ($H_1$)**: 효과가 존재하며, 연구자가 새롭게 입증하려는 주장입니다.

### 2) 의사결정 기준
* **유의수준 ($\alpha$)**: 귀무가설이 실제로 참인데도 이를 잘못 기각할 수 있는 허용 가능한 최대 확률 오류 한계입니다. (통상 0.05 설정, 즉 95% 신뢰수준)
* **p-value**: 귀무가설이 참이라고 가정할 때 현재 표본 데이터 수준의 결과가 도출될 확률입니다.
  * **p-value < 유의수준 (0.05)**: 귀무가설 기각, 대립가설 채택 (통계적으로 유의미함)
  * **p-value $\ge$ 유의수준 (0.05)**: 귀무가설 기각 불가, 채택

---

## 2. 두 집단의 평균에 대한 가설 검정 (T-Test)

두 연속형 변수 집단 간의 통계적 평균 차이의 유무를 밝혀내는 검정입니다.

### 1) 독립표본 T-검정 (Independent T-Test)
서로 무관한 독립된 두 집단(예: A반과 B반의 키 비교)의 평균을 비교합니다.
* **가정 조건**:
  * **정규성**: 두 집단은 각각 정규분포를 만족해야 합니다. (Shapiro-Wilk 검정으로 확인. 단, 표본 수가 30개 이상이면 중심극한정리에 의해 정규분포를 따르는 것으로 간주합니다.)
  * **등분산성**: 두 집단의 분산이 같아야 합니다. (Levene 검정으로 평가합니다.)
* **정규성 불만족 시**: **맨 휘트니 U 검정 (Mann-Whitney U Test)**을 대체 사용하여 비모수 검정을 실시합니다.

```python
from scipy import stats

# 1. Shapiro-Wilk 정규성 검정 (H0: 정규성을 만족한다, 즉 p-value가 클수록 좋음)
print("A 정규성:", stats.shapiro(group_A))
print("B 정규성:", stats.shapiro(group_B))

# 2. Levene 등분산성 검정 (H0: 두 집단의 분산이 같다)
print("등분산성:", stats.levene(group_A, group_B))

# 3. 독립표본 T-검정 (equal_var=True면 등분산성 만족)
result = stats.ttest_ind(group_A, group_B, equal_var=True)
print("T-test 결과:", result)
```

### 2) 대응표본 T-검정 (Paired T-Test)
동일한 표본 집단을 대상으로 전후 상황(예: 다이어트 약물 복용 전과 복용 후의 체중 변화)의 평균 차이를 분석합니다.
* **정규성 검정의 차이**: 전후 각각에 대해 정규성을 보는 것이 아닌, **두 그룹의 차잇값(after - before)에 대해 Shapiro 정규성 검정**을 1회만 실시합니다.
* **정규성 불만족 시**: **윌콕슨 부호 순위 검정 (Wilcoxon Signed-Rank Test)**으로 비모수 대체하여 분석을 수행합니다.

```python
# 대응표본 T-검정
diff = df['after'] - df['before']
print("차잇값 정규성 검정:", stats.shapiro(diff))

# stats.ttest_rel API를 통해 분석 구동
result = stats.ttest_rel(df['before'], df['after'])
print("Paired T-test 결과:", result)
```

---

## 3. 두 집단의 비율에 대한 가설 검정 (범주형)

연속형 변수가 아닌 범주형 변수의 비율 차이 또는 두 요인 간의 연관성(독립성)을 평가할 때 교차표(Contingency Table)를 사용해 검정합니다.

### 1) 카이제곱 검정 (Chi-Square Test)
* **조건**: 교차표 상에서 계산된 모든 기대빈도가 5 미만인 셀의 비율이 전체의 20% 미만이어야 합니다.
* **`stats.chi2_contingency()`** API를 사용합니다.

### 2) 피어셔의 정확 검정 (Fisher's Exact Test)
* **대상**: 표본 데이터 수가 너무 적어 기대빈도가 5 미만인 셀이 교차표에 20% 이상 존재할 때, 카이제곱 검정을 대체해 정확한 확률을 연산하는 기법입니다.
* **`stats.fisher_exact()`** API를 활용합니다.
