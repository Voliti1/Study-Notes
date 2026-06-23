---
layout: post
date: 2026-05-06
title: 02. 제어문, 함수 및 객체지향 프로그래밍 (Control, Functions & OOP)
author: Voliti
category_name: python
subcategory: basic
---

## 1. 조건문과 반복문

### 1) 조건문 (if, elif, else)
주어진 조건을 평가하여 코드 블록을 분기합니다. C언어의 `else if`와 달리 파이썬은 `elif` 키워드를 사용합니다.
```python
score = int(input("점수를 입력해주세요: "))
if score >= 90:
    print("A등급")
elif score >= 80:
    print("B등급")
else:
    print("C등급")
```

### 2) 반복문 (while, for)
* **while**: 조건이 참인 동안 코드를 무한 반복하며, 이탈 키워드(`break`)와 스킵 키워+드(`continue`)로 제어합니다.
* **for**: 지정한 시퀀스 또는 `range()` 범위 내에서 순회합니다.

### 3) 파이썬만의 특수 구문: for - else
* **특징**: for 반복문이 중간에 `break`로 인해 끊기지 않고 **마지막 범위까지 완전히 정상 순회했을 때만** 하단의 `else` 블록이 실행됩니다.
```python
for i in range(2):
    print(i)
else:
    print("정상 종료 (done)") # break가 발생하지 않았으므로 실행됨
```

---

## 2. 함수와 변수 스코프 (Variable Scopes)

### 1) 함수 선언 및 호출
* `def` 키워드로 선언하며, 반환값이 명시되지 않으면 자동으로 `None` 객체를 돌려줍니다.

### 2) 변수 검색 규칙 (LEGB Rule)
파이썬은 변수를 찾을 때 다음 우선순위를 거쳐 탐색을 수행합니다:
1. **Local (L)**: 함수 내부의 가장 좁은 지역 스코프
2. **Enclosing (E)**: 중첩 함수 구조에서 내부 함수를 감싸는 외부 함수의 영역
3. **Global (G)**: 모듈 파일 전역 수준의 스코프
4. **Built-in (B)**: 파이썬 인터프리터 자체에 내장된 기본 식별자 영역

### 3) global & nonlocal 키워드
* **`global`**: 함수 내에서 전역 변수를 새로 선언하거나 값을 직접 수정할 때 명시합니다. (`global` 없이 대입 연산 시 별개의 지역 변수가 내부적으로 선언됩니다.)
* **`nonlocal`**: 내부 함수에서 외부 함수의 변수를 수정하려고 할 때 명시합니다. (반드시 외부 함수 영역에 해당 변수가 이미 선언되어 있어야 오류가 나지 않습니다.)

```python
# nonlocal 실습 예시
def outer_function():
    count = 10
    
    def inner_function():
        nonlocal count # 외부 함수의 count 변수를 직접 수정
        count += 5
        print(f"내부 함수 count: {count}")
        
    inner_function()
    print(f"외부 함수 count: {count}")

outer_function()
# 출력 결과:
# 내부 함수 count: 15
# 외부 함수 count: 15
```

---

## 3. 객체지향 프로그래밍 (OOP) & 클래스

파이썬의 모든 것은 객체(Object)이며, 객체를 생성하기 위한 템플릿인 클래스(Class)를 제공합니다.

### 1) 생성자 (`__init__`) 및 인스턴스화
* 생성자는 클래스를 메모리에 객체 형태로 실체화(Instantiation)할 때 자동으로 호출되는 특수 목적 메서드입니다. 첫 번째 인자는 관습적으로 자기 참조 변수인 `self`를 받습니다.
* **객체 생성**: 생성자 메서드명인 `__init__`을 직접 호출하지 않고, 클래스명에 괄호를 붙여 생성합니다. (초보자들이 흔히 헷갈리는 부분입니다.)

### 2) 상속과 부모 메서드 호출 (`super()`)
자식 클래스를 생성해 부모의 기능을 물려받거나 추가로 정의할 수 있으며, `super()` 키워드를 사용해 부모 클래스의 생성자나 메서드를 명시적으로 불러올 수 있습니다.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"안녕하세요, 저는 {self.name}이고 {self.age}살입니다.")

# Person을 상속받는 Worker 클래스
class Worker(Person):
    def __init__(self, name, age, job):
        super().__init__(name, age) # 부모 클래스 생성자 호출
        self.job = job

    def introduce(self):
        super().introduce() # 부모 메서드 실행
        print(f"직업은 {self.job}입니다.")

worker = Worker("Alice", 30, "엔지니어") // 인스턴스화
worker.introduce()
```

---

## 4. 타입 시스템 및 예외 처리 (try-except)

### 1) 타입 안정성과 검사 시점
* **동적 타입 검사(Dynamic Typing)**: 파이썬은 변수의 타입이 실행 시점(런타임)에 유연하게 검증되는 인터프리터의 특성을 가집니다.
* **강타입 언어(Strongly Typed)**: 약타입 언어(JavaScript 등)와 달리 암묵적인 형 변환을 제한합니다. 예를 들어 문자열과 숫자의 덧셈 연산(`"score: " + 90`)은 자료형이 엄격히 유지되어 에러를 발생시킵니다.

### 2) 예외 처리
시스템의 갑작스러운 중단을 방지하기 위해 파일 I/O 및 데이터베이스 연동부 등에서 `try - except - else - finally` 문을 구성하여 런타임 오류에 방어적인 코드를 작성합니다. 또한 `raise` 키워드를 사용해 특정 유효성에 위배될 경우 수동으로 에러 객체를 던질 수 있습니다.

---

## 5. 파이썬 코딩 관례 (PEP 8)

* **명명 규칙**:
  * 변수 및 함수명: `snake_case` (예: `user_name`, `get_data`)
  * 클래스명: `PascalCase` (예: `PersonInfo`, `DbManager`)
  * 상수: `UPPER_CASE` (예: `MAX_LIMIT`, `PI`)
* **임포트 순서**:
  1. 표준 라이브러리 (Standard Library)
  2. 서드파티 라이브러리 (Third-party e.g. Pandas, NumPy)
  3. 로컬 프로젝트 라이브러리
* **코드 스타일 검사 자동화 도구**:
  * **flake8**: 코드 포맷 스타일 오류 검사기.
  * **black**: 코드를 강제 규격화하여 자동 포맷해주는 강력한 도구.
  * **pylint**: 코드 전체적인 버그 가능성과 품질 지수를 평가하는 검사기.
