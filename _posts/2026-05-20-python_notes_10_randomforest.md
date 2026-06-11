---
layout: post
date: 2026-05-20
title: 10. 앙상블과 랜덤 포레스트 (Ensemble & Random Forest)
author: Voliti
category_name: python
---

단일 결정트리 모델은 구조가 직관적이고 해석이 쉬우나 과대적합(Overfitting)에 매우 취약하다는 단점이 있음. 이를 해결하기 위해 여러 개의 독립적인 모델(결정트리)을 결합하여 개별 예측 결과를 평균내거나 다수결로 종합하는 기법인 **앙상블 학습(Ensemble Learning)**을 도입함. 그 중 가장 널리 쓰이는 앙상블 알고리즘이 **랜덤 포레스트(Random Forest)**임.

---

## 1. 랜덤 포레스트의 기본 개념

### 1) 배깅 (Bagging, Bootstrap Aggregating)
- 전체 데이터셋에서 중복 허용 복원 추출 방식을 통해 여러 개의 부분 데이터셋(Bootstrap sample)을 생성함.
- 개별 결정트리 모델들을 이 부분 데이터셋으로 각각 독립 학습시킨 후, 다수결을 모아 최종 결과를 결정하는 방식임.

### 2) 특성 무작위 선택 (Random Feature Selection)
- 각 결정트리를 훈련시킬 때 전체 특성(Feature) 중에서 일부 특성만을 무작위로 선택하여 분할 기준으로 삼음.
- 이 과정을 통해 각 트리 간의 상관관계를 낮추어 모델의 다양성을 극대화하고 일반화 성능을 대폭 향상함.

---

## 2. 파이썬 실습: 과일 및 채소 종류 분류

### 1) 데이터 로드 및 분할
무게, 길이, 색상, 당도 데이터를 바탕으로 과일 종류를 분류하는 모델을 구축함.

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# 데이터 로드
src_data = pd.read_csv('./머신러닝실습용자료/과일채소목록.csv', encoding='cp949')

# 특성과 타겟 정의
data = src_data[["무게_g", "길이_cm", "색상", "당도"]]
target = src_data.종류

# 데이터 분 분리 (80:20)
훈련용_data, 테스트용_data, 훈련용_target, 테스트용_target = train_test_split(
    data, target, test_size=0.2, random_state=40
)
```

### 2) 랜덤 포레스트 모델 정의 및 학습
`n_estimators=10` 옵션을 지정하여 총 10개의 결정트리로 이루어진 랜덤 포레스트 모델을 생성함.

```python
from sklearn.ensemble import RandomForestClassifier

# 모델 생성 및 학습
rfc = RandomForestClassifier(n_estimators=10, n_jobs=-1, random_state=40)
rfc.fit(훈련용_data, 훈련용_target)

# 테스트 세트 예측값 및 정확도 평가
print("예측값:", rfc.predict(테스트용_data))
print("테스트용 정확도 점수:", rfc.score(테스트용_data, 테스트용_target))
```

**실행 결과:**
```
예측값: ['자두' '수박' '거봉포도' '참외' '거봉포도' '수박' '옥수수' '수박' '참외' '수박']
테스트용 정확도 점수: 1.0
```

---

## 3. 상세 모델 성능 평가

정확도 외에도 정밀도(Precision), 재현율(Recall), F1-Score 등 다각도의 성능 지표를 분석하기 위해 `classification_report`를 출력함.

```python
from sklearn.metrics import classification_report

pred = rfc.predict(테스트용_data)
print(classification_report(테스트용_target, pred))
```

**실행 결과:**
```
              precision    recall  f1-score   support

        거봉포도       1.00      1.00      1.00         2
          수박       1.00      1.00      1.00         4
         옥수수       1.00      1.00      1.00         1
          자두       1.00      1.00      1.00         1
          참외       1.00      1.00      1.00         2

    accuracy                           1.00        10
   macro avg       1.00      1.00      1.00        10
weighted avg       1.00      1.00      1.00        10
```
- 모든 범주에서 정밀도와 재현율 **1.00**을 기록하며 성공적인 모델 적합 결과를 보임.

---

## 4. 특성 중요도 (Feature Importance)

랜덤 포레스트 모델은 각 결정트리에서 분할 기준(노드 분할)으로 활용되면서 불순도를 줄이는데 얼마나 크게 기여했는지를 수치화한 **특성 중요도(Feature Importance)** 지표를 제공함.

```python
# 특성 중요도 값 출력
print("특성 중요도 지표:", rfc.feature_importances_)
```

**실행 결과:**
```
특성 중요도 지표: [0.43788379 0.18804429 0.15510803 0.21896389]
```

![랜덤 포레스트 특성 중요도 바차트]({{site.baseurl}}/assets/images/random_forest_feature_importance.png)

- **해석**: 각 특성의 분류 기여도를 확인한 결과 **무게_g (약 43.8%)** 특성이 과일 및 채소 종류를 구분하는 데 가장 결정적인 변수로 작용하였으며, 그 뒤를 이어 **당도 (약 21.9%)**, **길이_cm (약 18.8%)**, **색상 (약 15.5%)** 순서로 기여도가 높게 나타남.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
