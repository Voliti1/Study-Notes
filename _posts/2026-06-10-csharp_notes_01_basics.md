---
layout: post
date: 2026-06-10
title: 01. C# 프로그래밍 기초 (C# Basics)
author: Voliti
category_name: csharp
---

## 1. C#의 특징 및 환경 구성

C#은 Microsoft에서 개발한 강타입 기반의 형식 안정(Type-Safe)적인 객체지향 프로그래밍 언어입니다.

### 1) 주요 특징
* **형식 안정성(Type-Safe)**: 잘못된 타입의 연산이나 할당을 컴파일 또는 런타임에 완벽히 방지하여 런타임 신뢰성이 높습니다.
* **객체지향(OOP) 중심**: C#은 모든 코드가 클래스 내부에 작성되어야 하며 강력한 객체지향 원칙을 준수합니다.
* **구조적 계층**: `Solution > Project > Namespace > Class > Member(Variables, Methods)`의 명확한 포함 관계를 갖습니다.
  * **솔루션(Solution)**: 프로젝트들을 묶어서 종합 관리하는 단위입니다.
  * **프로젝트(Project)**: 애플리케이션 개발에 필요한 소스코드, 리소스 파일의 모음입니다.

---

## 2. 식별자와 기본 입출력

### 1) 명명 관례(Naming Convention)
* **PascalCase**: 클래스명, 메서드명, 속성(Property)명, 네임스페이스명 (예: `Program`, `Main`, `ConsoleApp`)
* **camelCase**: 지역 변수명, 매개변수명 (예: `inputName`, `elapsedTime`)
* **상수 및 정적 필드**: PascalCase를 기본으로 권장하며 기업이나 표준에 따라 접두어를 덧붙이기도 합니다.

### 2) 기본 입출력
* **`Console.Write()`**: 줄 바꿈 없이 출력합니다.
* **`Console.WriteLine()`**: 출력 후 자동으로 줄을 바꿉니다.
* **`Console.ReadLine()`**: 사용자로부터 콘솔 입력을 한 줄 읽어옵니다. (반환 타입은 무조건 `string`)

```csharp
using System; // C언어의 #include와 같은 역할

namespace BasicCSharp
{
    class Program
    {
        static void Main(string[] args) // 시작점 메서드
        {
            Console.Write("이름을 입력하세요: ");
            string name = Console.ReadLine();
            Console.WriteLine($"안녕하세요, {name}님!"); // 보간법 문자열 ($)
        }
    }
}
```

---

## 3. 데이터 타입 및 연산자

C#의 데이터 타입은 정적 타이핑 언어로서 메모리 크기가 엄격히 정해져 있습니다.

### 1) 자료형 분류 및 크기
* **문자**: `char` (2byte, 유니코드 대응)
* **정수**: `int` (4byte), `long` (8byte, 리터럴 뒤에 `L` 표시)
* **실수**: `float` (4byte, 리터럴 뒤 `f`), `double` (8byte, 기본값), `decimal` (16byte, 금융 연산용 초고정밀, 리터럴 뒤 `m`)
* **불 자료형**: `bool` (1byte, 참/거짓을 의미하며 **첫 글자는 반드시 소문자인 `true`, `false`**여야 함)
* **var 키워드**: 컴파일러가 자료형을 자동으로 판단합니다. (단, **지역 변수이면서 선언과 동시에 초기화할 때만 사용 가능**하며, 결정된 타입은 변경이 불가능합니다.)

### 2) 데이터 변환 및 소수점 포맷
* **강제 형변환(Casting)**: 크기가 큰 데이터 타입에서 작은 타입으로 변환할 때 데이터 유실이 발생할 수 있습니다. (예: `(int)10.5`)
* **문자열 파싱**: `타입.Parse(문자열)` 방식(예: `int.Parse("123")`)은 입력 데이터가 `null`일 경우 런타임 오류가 발생하므로 유효성 검증이 필요합니다.
* **Convert 클래스**: `Convert.ToInt32()` 등은 `null`을 에러 대신 `0`으로 유연하게 변환합니다.
* **ToString 포맷**: `number.ToString("0.00")` 형식으로 소수점 자리수를 지정할 수 있습니다.

---

## 4. 제어문 (조건문과 반복문)

### 1) 조건문
* **if - else if - else**: 복합적인 다중 조건 분기에 사용합니다.
* **switch - case**: JDK나 C/C++에 비해 C#은 switch 문에 문자열을 바로 매칭할 수 있는 유연성을 제공합니다.
* **ReadKey**: `Console.ReadKey()`를 사용하면 키보드 한 번의 클릭을 감지하여 동작을 결정할 수 있습니다.

### 2) 반복문
* **for / while / do-while**: 일반적인 제어 및 반복 흐름입니다.
* **foreach**: 배열이나 리스트와 같은 컬렉션의 첫 요소부터 끝 요소까지 안전하게 반복 실행하며, 컬렉션의 인덱스 이탈 오류를 차단합니다.

```csharp
using System;

class ControlFlow
{
    static void Main()
    {
        string[] seasons = { "봄", "여름", "가을", "겨울" };
        
        // foreach를 사용한 리스트 순회
        foreach (string season in seasons)
        {
            Console.WriteLine($"내가 좋아하는 계절: {season}");
        }
    }
}
```
