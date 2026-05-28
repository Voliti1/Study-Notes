---
layout: post
date: 2026-05-01
title: 01_01. 숫자형과 연산자
author: Voliti
---
### 숫자형(Number)

**Int**
- 정수 저장하는 자료형
- ex) 0, -1, 1

**Float**
- 실수 저장하는 자료형
- Float는 Floating Point(부동소수점)에서 따옴
- ex) 0.0, -1.2, 123.456
- 지수표현 방식도 사용 가능

### Operator(연산자)

- 덧셈 : +
- 뺄셈 : -
- 곱셈 : *
- 나눗셈 : /
- 몫 : //
- 나머지 : %
- 제곱 : **
### 연산자 우선순위
1. 제곱 연산자
2. 곱셈, 나눗셈, 나머지, 몫 연산자
3. 덧셈, 뺄셈 연산자
4. 괄호()를 통해 우선순위 변경 가능

### 복합 연산자
- a += b : a = a + b와 같음
- a -= b : a = a - b와 같음
- a *= b : a = a * b와 같음
- a /= b : a = a / b와 같음
- a //= b : a = a // b와 같음
- a %= b : a = a % b와 같음
- a **= b : a = a ** b와 같음

```python
a = 3; b = 2
print("a =", a ,"b =", b)
print("a + b =", (a + b))
print("a - b =", (a - b))
print("a * b =", (a * b))
print("a / b =", (a / b))
print("a // b =", (a // b))
print("a % b =", (a % b))
print("a ** b =", (a ** b))

```
**실행 결과:**
```
a = 3 b = 2
a + b = 5
a - b = 1
a * b = 6
a / b = 1.5
a // b = 1
a % b = 1
a ** b = 9
```


### 비교 연산자
값의 비교를 통해 True, False의 값을 얻을 수 있는 연산자
- a == b a와 b가 같다
- a != b a와 b가 다르다
- a \> b a가 b보다 크다
- a < b a가 b보다 작다
- a <= b a가 b보다 작거나 같다
- a \>= b a가 b보다 크거나 같다

```python
x = 1
y = 2

print("x==y: "+str(x == y))
print("x!=y: "+str(x != y))
print("x>y: "+str(x > y))
print("x<y: "+str(x < y))
print("x<=y: "+str(x <= y))
print("x>=y: "+str(x >= y))
```
**실행 결과:**
```
x==y: False
x!=y: True
x>y: False
x<y: True
x<=y: True
x>=y: False
```

### 논리 연산자
논리 연산시 사용하는 연산자
- and
- or
- not

```python
a = True
b = False

print("True and True: "+str(a and a))
print("True and False: "+str(a and b))
print("False and True: "+str(b and a))
print("False and False: "+str(b and b))

print("True or True: "+str(a or a))
print("True or False: "+str(a or b))
print("False or True: "+str(b or a))
print("False or False: "+str(b or b))

# not 연산자
print("not True: "+str(not a))
print("not False: "+str(not b))
```
**실행 결과:**
```
True and True: True
True and False: False
False and True: False
False and False: False
True or True: True
True or False: True
False or True: True
False or False: False
not True: False
not False: True
```