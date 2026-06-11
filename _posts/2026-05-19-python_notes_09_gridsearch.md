---
layout: post
date: 2026-05-19
title: 09. 그리드 서치 (Grid Search)
author: Voliti
category_name: python
---

머신러닝 모델의 성능을 최적화하기 위해서는 사용자가 직접 설정해 주어야 하는 매개변수인 **하이퍼파라미터(Hyperparameter)**를 적절하게 튜닝해야 함. 이를 수동으로 일일이 변경하며 검증하는 것은 비효율적이므로, 탐색하고자 하는 하이퍼파라미터 후보들의 값을 격자(Grid) 형태로 나열하고 교차검증을 통해 최적의 조합을 자동 탐색하는 **그리드 서치(Grid Search)** 기법을 활용함.

---

## 1. 그리드 서치 및 GridSearchCV 개념

### 1) 작동 원리
- 사용자가 하이퍼파라미터 후보들을 지정함 (예: `{'max_depth': [1, 2, 3]}`).
- 각 하이퍼파라미터의 모든 경우의 수(조합)에 대해 모델 학습 및 내부 교차검증(Cross Validation)을 수행함.
- 교차검증 성능 점수가 가장 높은 하이퍼파라미터 조합을 선정하고, 전체 훈련 데이터를 활용해 최종 모델을 재학습시킴.

### 2) scikit-learn의 GridSearchCV
- `GridSearchCV` 클래스는 교차검증 기능(CV)과 그리드 서치(Grid Search)를 하나로 묶어 제공함.
- `n_jobs=-1` 설정을 통해 컴퓨터의 모든 CPU 코어를 병렬 동원함으로써 하이퍼파라미터 연산 속도를 높일 수 있음.

---

## 2. 파이썬 실습: 의사결정나무 하이퍼파라미터 최적화

### 1) 데이터 로드 및 훈련/테스트 데이터셋 분리
과일(수박/참외) 데이터를 로드하고 학습할 준비를 마침.

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# 데이터 로드
src_data = pd.read_csv('./머신러닝실습용자료/의사결정나무_과일종류_2가지.csv', encoding='cp949')

# 특성 및 타겟 추출
data = src_data[["무게", "길이"]].to_numpy()
target = src_data["종류"].to_numpy()

# 데이터 분리
훈련용_data, 테스트용_data, 훈련용_target, 테스트용_target = train_test_split(
    data, target, test_size=0.2, random_state=40
)
```

### 2) 단일 하이퍼파라미터 탐색 (`max_depth`)
의사결정트리의 최대 깊이(`max_depth`) 후보 `[1, 2, 3]` 중 최적의 값을 찾음.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

# 탐색할 매개변수 그리드 설정
parm = {'max_depth': [1, 2, 3]}

# 그리드서치 객체 정의 (DecisionTree 모델, 파라미터 그리드 적용)
gs = GridSearchCV(DecisionTreeClassifier(random_state=50), parm, n_jobs=-1)
gs.fit(훈련용_data, 훈련용_target)

# 최적의 매개변수 및 성능 확인
print("최적의 하이퍼파라미터:", gs.best_params_)
```

**실행 결과:**
```
최적의 하이퍼파라미터: {'max_depth': 1}
```

- 최적의 파라미터로 학습된 최종 의사결정트리 모델을 꺼내 훈련 세트의 정확도를 측정함.

```python
dt = gs.best_estimator_
print("최적 모델의 훈련용 정확도 점수:", dt.score(훈련용_data, 훈련용_target))
```

**실행 결과:**
```
최적 모델의 훈련용 정확도 점수: 1.0
```

---

## 3. 다중 하이퍼파라미터 탐색

여러 개의 하이퍼파라미터를 동시에 조합하여 다차원 탐색을 진행함.
- `max_depth`: `1`부터 `9`까지의 정수 (최대 깊이)
- `min_impurity_decrease`: `0.0001`부터 `0.0009`까지 `0.0001` 단위 실수 (최소 정보이득 감소량)
- `min_samples_split`: `2`부터 `92`까지 `10` 단위 정수 (노드를 분할하기 위한 최소 샘플 수)

```python
# 다중 파라미터 범위 설정
parm_multi = {
    'max_depth': range(1, 10, 1),
    'min_impurity_decrease': np.arange(0.0001, 0.001, 0.0001),
    'min_samples_split': range(2, 100, 10)
}

# 그리드서치 수행
gs_multi = GridSearchCV(DecisionTreeClassifier(random_state=50), parm_multi, n_jobs=-1)
gs_multi.fit(훈련용_data, 훈련용_target)

print("최적의 다중 하이퍼파라미터:", gs_multi.best_params_)
```

**실행 결과:**
```
최적의 다중 하이퍼파라미터: {'max_depth': 1, 'min_impurity_decrease': 0.0001, 'min_samples_split': 2}
```

- 훈련 중에 도출된 최적의 교차검증 평균 점수(최고 성능)와 최종 테스트 점수를 출력하여 과적합 여부를 분석함.

```python
# 교차검증 최고 평균 점수
print("교차검증 최고 평균 점수:", np.max(gs_multi.cv_results_['mean_test_score']))

# 최종 성능 평가
best_dt = gs_multi.best_estimator_
print("최종 테스트 세트 정확도:", best_dt.score(테스트용_data, 테스트용_target))
print("최종 훈련 세트 정확도:", best_dt.score(훈련용_data, 훈련용_target))
```

**실행 결과:**
```
교차검증 최고 평균 점수: 0.8
최종 테스트 세트 정확도: 0.6666666666666666
최종 훈련 세트 정확도: 1.0
```
- 다중 파라미터 조합 탐색 결과 깊이가 1일 때 교차검증 평균 점수 **0.8**로 최적의 일반화 성능을 얻어냄.
- 다만, 전체 데이터 볼륨이 극히 적어 최종 테스트 세트 정확도는 0.667을 기록함. 데이터 양을 추가로 수집함으로써 평가 신뢰도를 향상할 수 있음.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
