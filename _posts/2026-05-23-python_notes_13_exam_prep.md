---
layout: post
date: 2026-05-23
title: 13. 시험대비 (Exam Preparation)
author: Voliti
category_name: python
subcategory: ai
---

본 정리글은 머신러닝 실기 시험 또는 평가를 대비하여 **데이터 전처리, 파생변수 생성, 변수 선택, 모델 학습, 모델 저장 및 실시간 예측 파이프라인**을 구축하는 일련의 과정을 정리한 내용입니다. 

훈련 데이터(`train.csv`)로 모델과 전처리 규칙을 생성하여 파일로 저장하고, 테스트 데이터(`test.csv`)가 들어왔을 때 저장된 규칙에 맞추어 실시간으로 예측을 수행한 뒤 최종 평가 점수(Macro Avg F1-Score)를 산출하는 정석적인 워크플로우를 다룹니다.

---

## 1. 모델 학습 및 규칙 저장 (Training Pipeline)

훈련 데이터(`train.csv`)를 활용하여 전처리, 변수 선택, 하이퍼파라미터 튜닝을 거쳐 최종 모델을 생성하고 필요한 규칙들을 `.pkl` 파일로 내보내는 과정입니다.

### 1) 데이터 로드 및 타겟 분리
학습 데이터를 불러오고 특징 행렬($X$)과 타겟 벡터($y$)로 분리합니다. 시험장에서 타겟 열의 위치가 변경되어 출제될 경우를 대비한 유연한 대처 코드가 포함되어 있습니다.

```python
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# 1. train.csv 데이터 로드
df_train = pd.read_csv('train.csv')

# 2. 데이터(X)와 타겟(y) 분리 및 설정 (기본값은 마지막 열이 타겟)
X_train = df_train.iloc[:, :-1]
y_train = df_train.iloc[:, -1]
```

> 🚨 **[시험장 돌발상황 대처]**
> 만약 타겟(정답) 열이 맨 끝이 아니라 중간이나 맨 앞에 섞여서 출제된 경우, 위 코드를 사용하지 않고 직접 타겟 컬럼명을 지정해야 합니다.
> ```python
> target_col_name = 'Class'  # <-- 시험지에 적힌 정확한 타겟 컬럼명 입력
> X_train = df_train.drop(columns=[target_col_name], errors='ignore')
> y_train = df_train[target_col_name]
> ```

### 2) 파생변수 생성 (위치 기준 자동 조립)
컬럼명이 복잡하게 출제되거나 이름을 모르는 경우를 대비하여, 컬럼의 **인덱스 위치**를 기준으로 파생변수를 안전하게 조합합니다.
- `base_col_name`: 마지막 컬럼 ($X_{last}$)
- `t1`, `t2`: 첫 번째, 두 번째 컬럼 ($X_0$, $X_1$)

```python
# 3. [파생변수 조합] 이름 몰라도 위치로 자동 조립
base_col_name = X_train.columns[-1] 
t1, t2 = X_train.columns[0], X_train.columns[1]

# 나눗셈 시 0으로 나누는 오류 방지를 위해 1e-3(0.001) 더해줌
X_train['New_Div_Feature'] = X_train[t1] / (X_train[base_col_name] + 1e-3)
X_train['New_Weighted_Feature'] = (X_train[t1] * 2.0) + X_train[t2]
```

### 3) 종합 연관성 평가 및 상위 5개 변수 선정
학습 데이터셋의 모든 독립변수에 대해 두 가지 방식으로 우선순위를 구하고 종합 점수를 산출합니다.
1. **상관관계 기반 순위**: 각 변수와 타겟($y$) 간의 피어슨 상관계수 절댓값 기준 순위 (`corr_rank`)
2. **랜덤 포레스트 변수 중요도 순위**: 기본적인 Random Forest 모델을 빠르게 학습시켜 얻은 중요도 순위 (`rf_rank`)
3. **종합 점수 계산**: 두 순위의 가중치 합(`corr_rank + rf_rank * 1.5`)이 낮은(즉, 순위가 높은) 상위 5개 변수를 선택합니다.

```python
# 4. 종합 연관성 순위 계산 및 상위 5개 '위치(인덱스 번호)' 추출
corr_rank = X_train.corrwith(y_train).abs().rank(ascending=False)

rf_final = RandomForestClassifier(n_estimators=50, class_weight='balanced', n_jobs=-1, random_state=40)
rf_final.fit(X_train.values, y_train.values) # .values로 이름 경고 방지
rf_rank = pd.Series(rf_final.feature_importances_, index=X_train.columns).rank(ascending=False)

# 종합 점수가 가장 낮은(우수한) 5개 컬럼의 실제 위치 번호(정수 인덱스)를 리스트로 추출
top_5_indices = (corr_rank + (rf_rank * 1.5)).sort_values().index[:5]
top_5_pos = [X_train.columns.get_loc(col) for col in top_5_indices]
```

### 4) 데이터 스케일링 및 모델 학습
선정된 5개 변수만 필터링한 후 `StandardScaler`를 활용하여 표준화 전처리를 수행하고, 데이터 불균형 문제를 완화하기 위해 하이퍼파라미터가 튜닝된 최종 Random Forest 모델을 학습합니다. 이때 경고창을 방지하고 일반화 성능을 높이기 위해 `.values`를 붙여 피처명을 지우고 학습합니다.

```python
# 5. 모델 학습 진행 (.values로 컬럼명 완전 제거)
X_train_final = X_train[top_5_indices].values 

final_scaler = StandardScaler()
X_train_scaled = final_scaler.fit_transform(X_train_final)

# 임계값 조정 없이 자체 밸런싱이 최적화된 모델 구축
best_model = RandomForestClassifier(
    n_estimators=300,            # 트리 개수를 확장하여 일반화 성능 극대화
    criterion='entropy',         # 불균형 데이터 대응력 강화
    max_features='sqrt',         # 정예 5개 변수 시너지 최적화
    min_samples_split=5,         # 분할 최소 샘플 수 제한으로 과적합 방지
    min_samples_leaf=2,          # 리프 노드 제한으로 처음 보는 데이터 방어력 증대
    class_weight='balanced',     # 소수 클래스 가중치 부여로 Macro F1 점수 사수
    n_jobs=-1, 
    random_state=40
)
best_model.fit(X_train_scaled, y_train.values) # 타겟에서도 이름을 제거하여 일관성 유지
```

### 5) 모델 및 전처리 파일 저장
테스트 환경에서도 동일한 스케일링 기준과 선택된 피처 위치를 활용할 수 있도록 모델과 객체들을 `joblib` 파일 형태로 저장합니다.

```python
# 6. 규칙 파일 보관
joblib.dump(best_model, 'best_rf_model.pkl')
joblib.dump(final_scaler, 'final_scaler.pkl')
joblib.dump(top_5_pos, 'top_5_pos.pkl')

print("=" * 60)
print("▶ [성공] 하이퍼파라미터가 안정화된 고성능 pkl 저장을 완료했습니다.")
print(f"▶ 선정된 열 위치 번호: {top_5_pos}")
print("=" * 60)
```

---

## 2. 실시간 예측 및 평가 (Inference Pipeline)

저장된 모델 및 전처리 규칙 파일(`.pkl`)을 호출하여 새로운 테스트 데이터(`test.csv`)가 입력되었을 때 일관성 있게 예측을 구동하고 점수를 채점하는 과정입니다.

### 1) 실시간 예측 함수 정의
훈련 단계에서 사용한 동일한 규칙(파생변수 생성식, 5개 중요 변수의 인덱스 위치, 학습된 StandardScaler 및 RandomForest 모델)을 사용하여 실시간 테스트 데이터셋을 가공하고 라벨을 예측합니다.

```python
# 4. [조건 4] 테스트 데이터 실시간 구동 환경 선구축
def predict_realtime_test_set(test_csv_path):
    # ① 실시간 테스트 데이터셋 로드
    df_test = pd.read_csv(test_csv_path)
    
    # 🚨 [시험장 대처] 평가용 파일에 정답(타겟) 열이 포함되어 있다면 전처리 전 미리 제거
    if 'Class' in df_test.columns:
        df_test_features = df_test.drop(columns=['Class'])
    elif 'target' in df_test.columns:
        df_test_features = df_test.drop(columns=['target'])
    else:
        df_test_features = df_test.copy()

    # ② [파생변수 조합] 훈련과 동일하게 인덱스 위치 기준으로 파생변수 생성
    base_col_name = df_test_features.columns[-1]
    t1, t2 = df_test_features.columns[0], df_test_features.columns[1]
    
    df_test_features['New_Div_Feature'] = df_test_features[t1] / (df_test_features[base_col_name] + 1e-3)
    df_test_features['New_Weighted_Feature'] = (df_test_features[t1] * 2.0) + df_test_features[t2]
    
    # ③ 규칙 파일(학습 때 선정된 5개 열의 위치 번호) 로드
    loaded_pos = joblib.load('top_5_pos.pkl')
    
    # ④ 위치(인덱스 숫자)를 기준으로 5개 열만 필터링 후 컬럼명 즉시 박멸 (.values)
    X_realtime = df_test_features.iloc[:, loaded_pos].values
    
    # ⑤ 스케일러 및 최종 머신러닝 모델 파일 로드
    loaded_scaler = joblib.load('final_scaler.pkl')
    loaded_model = joblib.load('best_rf_model.pkl')
    
    # ⑥ 훈련 데이터와 동일한 기준으로 스케일링 전처리 수행
    X_realtime_scaled = loaded_scaler.transform(X_realtime)
    
    # ⑦ 최종 라벨 예측 수행
    predictions = loaded_model.predict(X_realtime_scaled)
    
    return predictions
```

### 2) 테스트 데이터 예측 실행 및 평가 성적표 출력
실제 `test.csv` 데이터를 로드하여 성능을 산출합니다. 테스트 파일에 실제 정답 열이 포함되어 있다면 `classification_report`와 `Macro F1-Score`를 채점하여 출력하고, 정답 열이 없는 예측 전용 파일이라면 제출용 샘플을 출력합니다.

```python
# 5. [조건 5] 실제 test.csv 가동 및 기말고사 성적 채점
test_file_name = 'test.csv' 

print("▶ [가동] 컬럼명 완전 박멸형 실시간 테스트 데이터 구동을 시작합니다...")
final_predictions = predict_realtime_test_set(test_file_name)

# =========================================================================
# [결과 검증] Macro Avg F1-Score 성적표 출력
# =========================================================================
print("\n" + "="*60)
print("★ [최종 성적표] 실시간 구동 모델 성능 채점 결과")
print("="*60)

df_actual = pd.read_csv(test_file_name)

# 실제 타겟 컬럼명 자동 탐색
actual_target_col = None
for col in ['Class', 'target', df_actual.columns[-1]]:
    if col in df_actual.columns:
        actual_target_col = col
        break

if actual_target_col:
    from sklearn.metrics import classification_report, f1_score
    y_actual = df_actual[actual_target_col]
    print(classification_report(y_actual, final_predictions, digits=4))
    macro_f1 = f1_score(y_actual, final_predictions, average='macro')
    print("-"*60)
    print(f"🎯 교수님 제출용 기말고사 최종 평가 점수 (Macro F1): {macro_f1:.4f}")
    print("="*60)
else:
    print("▶ [안내] test.csv에 정답 열이 존재하지 않아 예측 라벨 출력으로 대체합니다.")
    print(f"▶ 최초 10개 예측 결과 샘플: {final_predictions[:10]}")
```

---

## 3. 핵심 요약 및 주의 사항

1. **컬럼명 제거 (`.values`)**: 피처 선택이나 가공 시 컬럼 순서나 이름에 변동이 생기면 스케일러나 모델이 오류(`feature_names mismatch`)를 발생시킵니다. 학습 및 예측 시 항상 `.values`를 붙여 넘파이 배열 형태로 학습 및 전처리하는 것이 안전합니다.
2. **`min_samples_leaf`, `class_weight='balanced'`**: 불균형이 심한 데이터(예: 이상 탐지, 부도 예측 등)에서는 다수 클래스에 모델이 편향되기 쉽습니다. 랜덤 포레스트의 `class_weight` 옵션과 리프 노드의 최소 샘플 제한을 설정해 소수 클래스의 재현율을 방어해야 시험 시 오차가 적습니다.
3. **위치 번호(`top_5_pos`) 기준 슬라이싱**: 새로운 테스트 셋에서 파생 변수를 추가하고 컬럼 인덱스가 바뀌더라도, 사전에 선정한 중요 피처 5개의 원래 순서대로 인덱스를 저장해 놓았으므로 (`top_5_pos.pkl`), 항상 정확한 변수만 슬라이싱해올 수 있습니다.

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
