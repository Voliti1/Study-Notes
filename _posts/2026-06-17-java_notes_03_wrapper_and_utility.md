---
layout: post
date: 2026-06-17
title: 3. Wrapper 클래스 및 형변환
author: Voliti
category_name: java
---

Java에서 기본 타입(Primitive Type) 데이터를 객체로 래핑하여 제네릭 컬렉션 등에서 다룰 수 있게 해주는 Wrapper 클래스 및 유틸리티 연산 정리입니다.

---

## 1. Wrapper 클래스와 박싱/언박싱

* **대응 관계**: `int - Integer`, `char - Character`, `double - Double`, `boolean - Boolean` 등.
* **박싱(Boxing)**: 기본 타입 값을 Wrapper 객체로 만드는 과정.
* **언박싱(Unboxing)**: Wrapper 객체에서 기본 타입 값을 추출하는 과정.
* **오토박싱/오토언박싱**: Java 컴파일러가 자동으로 형변환해 줍니다.
  ```java
  Integer num = 17; // 자동 박싱
  int n = num;      // 자동 언박싱
  ```

---

## 2. 문자열 및 숫자 간 형변환

* **문자열 -> 숫자**: `Integer.parseInt("123")`, `Double.parseDouble("12.3")`
* **숫자 -> 문자열**: `String.valueOf(123)` 또는 `Integer.toString(123)`

---

## 3. Switch Expressions (JDK 14 이상)

기존 콜론(`:`) 및 `break`문을 사용하던 switch문을 대체하여 화살표(`->`) 지시자로 분기를 단축하고 간결하게 표현하며 반환값을 바로 대입할 수 있는 향상된 구문입니다.

```java
int scoreGroup = (int)(avg / 10);
switch (scoreGroup) {
    case 10, 9 -> System.out.println("A");
    case 8     -> System.out.println("B");
    default    -> System.out.println("F");
}
```

---

## 4. JDBC MySQL 데이터베이스 연동

자바 애플리케이션에서 데이터베이스에 통신하여 쿼리를 수행하기 위해 외부 라이브러리인 MySQL Connector JAR을 탑재하여 연결 객체를 여는 전형적인 양식입니다.

```java
import java.sql.Connection;
import java.sql.DriverManager;

public class DbConnect {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/library";
        String user = "root";
        String password = "password";
        
        try {
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("데이터베이스 연결 성공!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
