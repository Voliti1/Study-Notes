---
layout: post
date: 2026-05-03
title: 01_03. 문자열
author: Voliti
---
### 문자열(String)
- 문자들의 집합, 문자, 단어의 모임
- 'string', "string", '''string''', """string"""의 4가지 방법

#### Escape Code
- \n - 줄바꿈 
- \t - 탭 간격 생성
- \\' - ' 표현 
- \\" - " 표현 
- \\\ - \ 표현 
- 활용 빈도가 높은 5가지

```python
a = "Just\n do it!!"
b = "010\t1234\t5678"
c = "\'   \"   \\  "
print(a); print(b); print(c)
```
**실행 결과:**
```
Just
 do it!!
010	1234	5678
'   "   \
```

### 문자열 연산
- #### 문자열 더하기

```python
a = "Python"
b = " is fun"

print(a + b)
```
**실행 결과:**
```
Python is fun
```

- #### 문자열 곱하기

```python
a = "Python"
print(a * 2)
```
**실행 결과:**
```
PythonPython
```
#### 문자열 Indexing

* [I][\t][l][i][k][e][\t][g][a][m][e]
* [0][1][2][3][4][5][6 ][7][8][9][10]
* [-11][-10][-9].....[-4][-3][-2][-1]

```python
g = "I like game"

a = g[0]
b = g[-11]
print(a); print(b)

c = g[1]
print(c)

d = g[-4] + g[-3]+ g[-2] + g[-1]
print(d)
```
**실행 결과:**
```
I
I
 
game
```

#### 문자열 Slicing
문자열을 원하는 지점부터 원하는 크기만큼 분해

- 변수명[첫번째 항목 인덱스:마지막 항목 인덱스 + 1]
- 마지막 항목 + 1로 지정하는 것이 매우 중요
- 첫번째 항목 인덱스를 설정하지 않으면, 0번 인덱스부터 추출
- 마지막 항목 인덱스를 설정하지 않으면, 마지막 항목까지 추출

```python
text = "I like Kimchi"
print(text[2:6])
print(text[7:13])
print(text[7:])
print(text[:6])
```
**실행 결과:**
```
like
Kimchi
Kimchi
I like
```

### 문자열 관련 함수
- LEN() : 문자열 길이 구하기
- COUNT() : 특정 문자 수 세기
- UPPER() : 모든 문자 대문자로 변경
- LOWER() : 모든 문자 소문자로 변경
- STRIP() : 양쪽 공백 지우기
- LSTRIP() : 왼쪽 공백 지우기
- RSTRIP() : 오른쪽 공백 지우기
- SPLIT() : 문자열 원하는 형식으로 나누기
- REPLACE() : 문자열 원하는 문자열로 바꾸기
- JOIN() : 문자열 사이사이에 문자 삽입

#### LEN()
공백, Escape Code를 포함한 문자열의 길이를 구하는 함수
Escape Code의 경우 \t 를 하나의 문자로 취급

```python
text = "I like\tKimchi"

len(text)
```
**실행 결과:**
```
13
```

#### COUNT()
문자열에 속한 특정 문자의 개수를 세는 함수

```python
text = "I like Kimchi"
print(text.count('i'))
```
**실행 결과:**
```
3
```

#### UPPER()
대문자 변경
#### LOWER()
소문자 변경

```python
a = "upper"
b = "LOWER"
c = "HaLf"

print(a.upper())
print(b.lower())
print(c.upper())
print(c.lower())
```
**실행 결과:**
```
UPPER
lower
HALF
half
```

#### STRIP(), LSRTIP(), RSRTIP()
공백 지우는 함수

```python
text = " center "

print(text.strip()) # " center "
print(text.lstrip()) # "center "
print(text.rstrip()) # " center"
```
**실행 결과:**
```
center
center 
 center
```

#### SPLIT()
문자열을 특정 기준에 따라 분리
- 형식 미지정 : 공백, TAB, 엔터 기준 분리
- 형식 지정 : 형식에 맞춰 분리
- 분리된 결과 : 리스트 형식으로 저장

```python
text1 = "Split test setence"
print(text1.split())

text2 = "p,y,t,h,o,n"
print(text2.split(','))
```
**실행 결과:**
```
['Split', 'test', 'setence']
['p', 'y', 't', 'h', 'o', 'n']
```

#### REPLACE()
문자열을 원하는 문자열로 대체

```python
text = "I like Kimchi"
print("원래 문장 : "+ text, "\n바뀐 문장 : "+ text.replace("Kimchi", "Steak"))
print("원래 문장 : "+ text, "\n바뀐 문장 : "+ text.replace("I", "You"))

```
**실행 결과:**
```
원래 문장 : I like Kimchi 
바뀐 문장 : I like Steak
원래 문장 : I like Kimchi 
바뀐 문장 : You like Kimchi
```

#### JOIN()
문자열 사이사이에 특정 문자 삽입

```python
word = "python"
print((',').join(word))
```
**실행 결과:**
```
p,y,t,h,o,n
```

### 문자열 Formatting
문자열에서 변수나 값을 원하는 형식으로 출력
1. 숫자 대입  2. 문자 대입  3. 변수 통해 값 대입

### 문자열 Format Code

- %s : String(문자열)
- %c : Char(문자 1개)
- %d : Int(정수)
- %f : Float(실수)
- %o : 8진수
- %x : 16진수

```python
print("%d명의 학생이 교실에 있다" % 9)

print("나는 %s학과이다" % "반도체장비소프트웨어")

print("지금 온도는 %f도 이다" % 16.5)
```
**실행 결과:**
```
9명의 학생이 교실에 있다
나는 반도체장비소프트웨어학과이다
지금 온도는 16.500000도 이다
```

### 사용자 입력 함수 INPUT()
사용자에게 문자열을 입력받아 변수에 저장하는 함수

- 변수 = input("문자열을 입력하세요 : ")
- input으로 받은 모든 값은 string 형태로 변수에 저장되므로 다른 자료형으로 사용하려면 자료형 변환을 사용해야 한다

```python
a = int(input('정수를 입력해주세요:'))
b = float(input('실수를 입력해주세요:'))

print(a+b)
```
**실행 결과:**
```
6.4
```