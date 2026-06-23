---
layout: post
date: 2026-06-16
title: 2. 핵심 컬렉션 프레임워크 (ArrayList, Map, Set)
author: Voliti
category_name: java
---

Java 컬렉션 프레임워크(Collection Framework)는 다수의 데이터를 효율적으로 처리하기 위해 표준화된 클래스들의 집합입니다. 기본형 타입(Primitive Type)은 담을 수 없으며 Wrapper 클래스나 참조형 객체만 저장할 수 있습니다.

---

## 1. ArrayList

가변 크기 배열로, 중간에 데이터를 삽입하거나 삭제할 수 있으며 자동으로 메모리 크기가 증대되는 동적 배열 자료구조입니다.

```java
import java.util.ArrayList;

public class ListExample {
    public static void main(String[] args) {
        ArrayList<String> strList = new ArrayList<>();
        strList.add("java"); // 추가
        strList.add(0, "python"); // 0번 인덱스에 삽입
        strList.remove(0); // 0번 인덱스 요소 삭제
        strList.set(0, "csharp"); // 값 수정
        int size = strList.size(); // 크기 조회
    }
}
```

---

## 2. HashMap (Map)

키(Key)와 값(Value)의 쌍으로 데이터를 관리하는 Dictionary 형태의 자료구조입니다. 키는 중복될 수 없고, 값은 중복을 허용합니다.

```java
import java.util.HashMap;

public class MapExample {
    public static void main(String[] args) {
        HashMap<String, String> map = new HashMap<>();
        map.put("사과", "apple"); // 등록
        System.out.println(map.get("사과")); // 값 검색 -> "apple"
        System.out.println(map.containsKey("당근")); // 키 존재 여부 -> false
        map.remove("사과"); // 삭제
    }
}
```

---

## 3. HashSet (Set) & 이터레이터 (Iterator)

### 1) HashSet
중복 저장을 절대 허용하지 않고, 순서가 없는 자료구조입니다. 집합 연산(교집합, 합집합, 차집합)을 직관적으로 수행할 수 있습니다.
* **교집합**: `s1.retainAll(s2);`
* **합집합**: `s1.addAll(s2);`
* **차집합**: `s1.removeAll(s2);`

### 2) 이터레이터 (Iterator)
컬렉션 내 요소를 순회하면서 안전하게 요소를 읽고 제거할 때 쓰는 탐색용 객체입니다.
```java
import java.util.HashSet;
import java.util.Iterator;

public class IteratorExample {
    public static void main(String[] args) {
        HashSet<String> set = new HashSet<>();
        set.add("apple");
        set.add("banana");

        Iterator<String> it = set.iterator();
        while(it.hasNext()) { // 읽을 다음 요소가 있다면
            System.out.println(it.next()); // 요소를 반환받아 출력
        }
    }
}
```
