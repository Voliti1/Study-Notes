---
layout: post
date: 2026-06-01
title: 14. 판다스 데이터 구조 및 기초 조작 (Pandas Basics)
author: Voliti
category_name: python
subcategory: bigdata
---

## 1. 판다스(Pandas) 자료구조 개요

판다스는 파이썬 환경에서 정형 및 반정형 데이터를 분석하기 위한 사실상의 표준 라이브러리입니다.

### 1) 자료구조의 차원성 비교
* **Series**: 1차원 배열 형태의 데이터 구조로, 단일 변수 데이터를 나타낼 때 사용합니다. (Numpy의 1차원 `ndarray`에 유연한 인덱스 레이블을 더한 구조)
* **DataFrame**: 행(Index)과 열(Column)로 구성된 2차원 테이블 데이터 구조로, 다중변수 데이터셋을 처리할 때 사용합니다.

---

## 2. 데이터 인덱싱 및 슬라이싱

데이터프레임 내의 특정 행과 열에 접근하여 값을 조회하는 두 가지 대표적 방식입니다.

### 1) iloc (Integer-based Location)
* **특징**: 행과 열의 0부터 시작하는 정수 번호(절대적 위치 위치)만을 기준으로 인덱싱합니다.
* **규칙**: 슬라이싱 기입 시 끝번호는 **포함하지 않습니다.** (`df.iloc[0:5]`는 0~4번 행 반환)

### 2) loc (Label-based Location)
* **특징**: 사용자가 직접 지정한 행의 레이블(이름) 또는 열의 이름을 기준으로 인덱싱합니다.
* **규칙**: 슬라이싱 기입 시 끝부분을 **포함합니다.** (`df.loc['John':'Tom']`은 Tom 행까지 반환)

```python
import pandas as pd

# 2차원 데이터프레임 선언 예시
score = pd.DataFrame(
    [[85, 96, 40], [73, 69, 45], [78, 50, 60]],
    index=['John', 'Jane', 'Tom'],
    columns=['Kor', 'Eng', 'Math']
)

# loc를 이용한 특정 값 조회
# score.columns[2]는 'Math'이므로 score.loc['Jane', 'Math']와 동일
print(score.loc['Jane', score.columns[2]]) // 45 출력
```

---

## 3. 데이터프레임 전처리 및 결측치 기초 연산

데이터 프레임에 변경을 가하거나 정렬하는 기본적인 API들입니다.

### 1) reset_index
* `drop = True`: 기존 인덱스 열을 데이터프레임 내에서 보존하지 않고 완전히 삭제합니다.
* `inplace = True`: 복사본 생성 없이 원본 데이터프레임 객체를 직접 갱신합니다. (Series 객체에서 `drop = False`와 `inplace = True`를 병행하면 반환 형식이 DataFrame이므로 형 충돌 에러가 날 수 있어 주의가 필요합니다.)

### 2) where와 dropna
* **`where(조건)`**: 조건식에 일치하는 데이터는 그대로 유지하고, 불일치하는 영역은 강제로 결측치(`NaN`)로 변경하여 마스킹합니다.
* **`dropna()`**: 결측치(`NaN`) 데이터 행 또는 열을 잘라내어 분석 대상에서 제거합니다.

```python
# 15도 이상의 데이터만 정상으로 남기고 나머지는 NaN 처리한 뒤 결측치 탈락
clean_temp = temp.where(temp >= 15).dropna()
```

### 3) 행/열의 삭제와 복사
* **`drop()`**: 행 또는 열을 제거할 때 사용하며, 원본에 반영하려면 `inplace=True` 혹은 `score = score.drop(...)` 형태로 갱신해야 합니다.
* **깊은 복사 (`copy()`)**: 얕은 복사(`score1 = score`)는 주소만 복제하여 한쪽을 수정하면 원본도 변경됩니다. 반면 `score.copy()`는 힙 메모리에 완전한 독립 객체를 새로 할당하여 독립적인 편집이 가능합니다.
