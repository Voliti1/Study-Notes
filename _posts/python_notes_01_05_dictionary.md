---
layout: post
title: 01_05. 딕셔너리
author: Voliti
---
### 딕셔너리 자료형
사전, key와 value를 한 쌍으로 가지는 자료형
- Key를 통해서 Value 값에 접근
- 순서가 없기 때문에, Indexing 및 Slicing이 불가능
- Key값은 고유한 값이므로 중복 불가

```python
dic1 = {'a': 'alpha', 'b': 'beta', 'g': 'gamma'}
dic2 = {1 : 'hello', 2 : [4, 5, 6], '3' : 9}

print(dic1)
print(dic2)
```
**실행 결과:**
```
{'a': 'alpha', 'b': 'beta', 'g': 'gamma'}
{1: 'hello', 2: [4, 5, 6], '3': 9}
```

### 딕셔너리 요소 추가 및 삭제
#### 추가
- 변수명[Key] = Value
#### 삭제
- del 변수명[Key]

```python
dic = {1 : 'one', 2 : 'two'}
print(dic)

dic[3] = 'three'
print(dic)

del dic[1]
print(dic)

print(dic[2])

test_dic = {1:'one', 2:'two', 2:'둘', 3:'셋', 3:'three', 3:'삼'}
print(test_dic)
```
**실행 결과:**
```
{1: 'one', 2: 'two'}
{1: 'one', 2: 'two', 3: 'three'}
{2: 'two', 3: 'three'}
two
{1: 'one', 2: '둘', 3: '삼'}
```

### 딕셔너리 관련 함수
 - keys() : key 리스트 만들기
 - values() : value 리스트 만들기
 - items() : key, value 쌍 리스트 얻기 (튜플형식)
 - clear() : 딕셔너리 초기화
 - get() : key값을 통해 value값 얻기
 - in : key가 딕셔너리에 있는지 찾아보기(true, false)

```python
dic = {'사과': 'apple', '바나나': 'banana', '메론': 'melon'}
print(dic.keys())
print(dic.values())
print(dic.items())

print(dic.get('바나나'))
print('사과' in dic)
print('수박' in dic)

dic.clear()
print(dic)
```
**실행 결과:**
```
dict_keys(['사과', '바나나', '메론'])
dict_values(['apple', 'banana', 'melon'])
dict_items([('사과', 'apple'), ('바나나', 'banana'), ('메론', 'melon')])
banana
True
False
{}
```