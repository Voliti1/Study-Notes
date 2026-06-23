---
layout: post
date: 2026-06-15
title: 1. 문자열 내장 메서드 및 StringBuilder
author: Voliti
category_name: java
---

Java의 `String`은 한번 생성되면 값을 변경할 수 없는 불변(Immutable) 객체입니다. 따라서 문자열을 수정하면 매번 새로운 문자열 객체가 힙 메모리에 생성되어 성능 오버헤드가 발생할 수 있습니다. 

이를 해결하기 위해 값의 수정이 빈번할 때는 가변(Mutable) 객체인 `StringBuilder`를 사용합니다.

---

## 1. 문자열 주요 내장 메서드

* **`equals()`**: 두 문자열의 실제 '값(내용물)'이 같은지를 정밀 비교합니다. 주소값을 비교하는 `==` 연산자와 다름에 유의해야 합니다.
  ```java
  String a = "hello";
  String b = new String("hello");
  System.out.println(a.equals(b)); // true
  System.out.println(a == b);      // false (주소가 다름)
  ```
* **`indexOf(str)`**: 문자열에서 특정 서브문자열이 시작되는 첫 번째 인덱스(위치)를 반환합니다. (없을 경우 `-1` 반환)
* **`contains(str)`**: 문자열에 특정 문자열이 포함되어 있는지 여부를 `true`/`false`로 반환합니다.
* **`charAt(index)`**: 지정된 인덱스 위치의 단일 문자(`char`)를 반환합니다.
* **`replaceAll(regex, replacement)`**: 정규식에 매칭되는 문자열을 포함하여 타겟 문자열을 지정 값으로 일괄 변경합니다.
* **`substring(start, end)`**: 시작 위치(start)부터 끝 위치(end) 직전까지의 부분 문자열을 슬라이싱합니다.
* **`split(separator)`**: 문자열을 구분자로 분할하여 문자열 배열(`String[]`)로 반환합니다.

---

## 2. StringBuilder 클래스

`StringBuilder`는 객체 내부 버퍼에 문자열을 저장하며, 새로운 객체를 계속 생성하지 않고 해당 버퍼 내에서 추가, 수정, 삭제 등의 편집을 수행합니다.

```java
StringBuilder sb = new StringBuilder();
sb.append("Hello"); // 문자열 추가
sb.insert(0, "Good "); // 0번 위치에 문자열 삽입
sb.delete(5, 7); // 5번부터 6번 인덱스까지의 문자 삭제
String result = sb.toString(); // 최종 String 타입 객체로 반환
```
