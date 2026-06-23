---
layout: post
date: 2026-05-18
title: 08. K-Fold 교차검증 (K-Fold Cross Validation)
author: Voliti
category_name: python
subcategory: ai
---

모델 학습 시 데이터를 단순히 훈련 세트(Train)와 테스트 세트(Test)로 한 번만 분할하여 모델을 검증하면 테스트 데이터에만 과적합되거나 데이터 우연성에 의해 점수가 불완전하게 평가받는 문제가 생길 수 있음. 이를 극복하기 위해 데이터를 여러 개의 그룹(Fold)으로 나누어 번갈아가며 모델을 교차 평가하는 **K-Fold 교차검증(K-Fold Cross Validation)** 기법을 활용함.

---

## 1. K-Fold 교차검증 작동 원리

### 1) 구조 및 단계
1. 전체 데이터셋을 동일한 크기를 가진 $K$개의 폴드(Fold, 그룹)로 분할함.
2. 1번째 폴드를 검증용(Validation) 데이터로 설정하고 나머지 $K-1$개 폴드를 훈련용 데이터로 삼아 모델을 학습하고 검증 점수를 산출함.
3. 이 과정을 2번째 폴드, 3번째 폴드... $K$번째 폴드까지 반복하여 총 $K$개의 검증 점수를 도출함.
4. $K$개 점수의 평균값을 최종 교차검증 점수로 판단함.

---

## 2. 파이썬 실습: 의사결정나무 모델 검증

### 1) 데이터 로드 및 훈련/테스트 데이터 분할
과일 종류(수박, 참외) 무게 및 길이 데이터를 활용하여 실습을 진행함.

```python
import pandas as pd
import numpy as np

# 데이터 로드
src_data = pd.read_csv('./머신러닝실습용자료/의사결정나무_과일종류_2가지.csv', encoding='cp949')

# 특성 및 타켓 분리
data = src_data[["무게", "길이"]].to_numpy()
target = src_data["종류"].to_numpy()

# 훈련용 및 테스트용 분할
from sklearn.model_selection import train_test_split
훈련용_data, 테스트용_data, 훈련용_target, 테스트용_target = train_test_split(
    data, target, test_size=0.2, random_state=40
)
```

### 2) 교차검증 미적용 모델 학습 및 결과
의사결정나무(`DecisionTreeClassifier`) 모델을 기본 학습시킨 성능을 점검함.

```python
from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=10)
dt.fit(훈련용_data, 훈련용_target)

print("훈련용 정확도 점수:", dt.score(훈련용_data, 훈련용_target))
print("테스트용 정확도 점수:", dt.score(테스트용_data, 테스트용_target))
```

**실행 결과:**
```
훈련용 정확도 점수: 1.0
테스트용 정확도 점수: 0.6666666666666666
```
- 데이터 개수가 매우 적어 훈련 데이터는 완벽하게 분류(1.0)하였으나, 테스트 데이터 정확도는 **0.667**로 크게 떨어지는 과대적합 경향을 보임.

---

## 3. 3-Fold 및 5-Fold 교차검증 적용

모델의 참된 성능을 알아보기 위해 훈련 데이터 내에서 K-Fold 교차검증을 적용함.

### 1) 3-Fold 교차검증 ($K=3$)
`cross_validate`와 `cross_val_score` 함수를 사용해 검증을 진행함.

```python
from sklearn.model_selection import cross_validate, cross_val_score

dt = DecisionTreeClassifier(random_state=10)

# cross_validate(): 학습 시간, 평가 점수 등 상세 결과 딕셔너리 반환
scores_1 = cross_validate(dt, 훈련용_data, 훈련용_target, cv=3)

# cross_val_score(): 각 검증 평가 점수들의 배열만 반환
scores_2 = cross_val_score(dt, 훈련용_data, 훈련용_target, cv=3)

print("교차검증 상세 결과:", scores_1)
print("3-Fold 평균 검증 정확도:", np.mean(scores_1['test_score']))
```

**실행 결과:**
```
교차검증 상세 결과: {'fit_time': array([0.0013, 0.    , 0.    ]), 'score_time': array([0.    , 0.002 , 0.    ]), 'test_score': array([1.  , 1.  , 0.66666667])}
3-Fold 평균 검증 정확도: 0.8888888888888888
```
- 3개 폴드에 대한 검증 점수(`[1.0, 1.0, 0.667]`)의 최종 평균 점수는 **0.889**로 측정됨.

### 2) 5-Fold 교차검증 ($K=5$)
```python
scores_5_fold = cross_val_score(dt, 훈련용_data, 훈련용_target, cv=5)

print("5-Fold 개별 검증 정확도:", scores_5_fold)
print("5-Fold 평균 검증 정확도:", np.mean(scores_5_fold))
```

**실행 결과:**
```
5-Fold 개별 검증 정확도: [1. 1. 1. 1. 0.]
5-Fold 평균 검증 정확도: 0.8

[Warning 발생]
UserWarning: The least populated class in y has only 3 members, which is less than n_splits=5.
```
- **경고 메시지 분석**: 현재 데이터셋 내 특정 클래스의 샘플 수가 폴드 수(5개)보다 작아 정상적인 5개 폴드 분할 및 계층 샘플링이 불가능함에 따른 안내 경고임. 
- 마지막 폴드의 정확도가 `0.0`으로 나온 이유는 훈련 데이터의 절대 부족으로 인해 학습 및 검증 과정에서 해당 폴드 내 정답 클래스가 전부 훈련셋 혹은 검증셋의 한쪽으로만 쏠려 모델이 올바르게 예측할 수 없었기 때문임. 
- 데이터셋의 규모와 특정 클래스의 고유 분포 개수(상대 빈도수)를 사전 파악하여 적절한 폴드 수($K$)를 채택해야 함.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
