---
layout: post
date: 2026-05-31
title: 02. C언어 고급 (Functions, Structs, Pointers & Files)
author: Voliti
category_name: c
---

## 1. 함수의 원형과 정의

C언어에서는 컴파일러가 위에서 아래로 해석하므로, 함수를 사용하기 전에 반드시 선언이 되어 있어야 합니다.

### 1) 함수 원형 선언과 정의 분리
main 함수 위쪽에 함수의 이름과 매개변수 타입을 정의하는 **함수 원형(Prototype) 선언**을 두고, main 함수 아래쪽에 **실제 본문을 정의**하는 관습을 가집니다.

```c
#include <stdio.h>

// 1. 함수 원형 선언
int add(int a, int b);

int main() {
    // 2. 함수 호출
    int sum = add(5, 10);
    printf("합계: %d\n", sum);
    return 0;
}

// 3. 실제 함수 정의
int add(int a, int b) {
    return a + b;
}
```

---

## 2. 포인터와 메모리 주소

### 1) 포인터 변수
* **포인터 변수 (`*`)**: 다른 변수의 메모리 주소를 저장하는 변수입니다.
* **주소 연산자 (`&`)**: 변수의 실제 메모리 주소값을 구합니다.
* **참조 해제 (`*`)**: 포인터 변수 앞에 붙어 해당 주소에 저장된 실제 값을 의미합니다.
* **배열명과 포인터**: C언어에서 배열의 이름은 상수 포인터와 같으므로, `int* num;`과 `int num[];`은 호환될 수 있습니다.

```c
#include <stdio.h>

int main() {
    int val = 10;
    int* ptr = &val; // ptr에 val의 주소 저장

    printf("val의 주소: %p\n", &val);
    printf("ptr이 가리키는 주소: %p\n", ptr);
    printf("ptr을 통한 실제값 접근: %d\n", *ptr);
    return 0;
}
```

---

## 3. 구조체 (Struct)

구조체는 하나 이상의 서로 다른 타입의 변수들을 묶어 새로운 사용자 정의 자료형을 만드는 도구입니다.

### 1) 구조체 정의와 별칭(typedef)
`struct` 선언 시 `typedef`를 함께 사용하면 구조체 변수를 선언할 때마다 `struct` 키워드를 매번 적지 않고 별칭을 사용해 간결하게 나타낼 수 있습니다.

```c
#include <stdio.h>

// 구조체 정의와 동시에 별칭(Point) 지정
typedef struct {
    int x;
    int y;
} Point;

int main() {
    Point p1; // struct Point p1; 이라고 생략 없이 쓸 필요 없음
    p1.x = 10;
    p1.y = 20;
    printf("좌표: (%d, %d)\n", p1.x, p1.y);
    return 0;
}
```

---

## 4. 파일 입출력 및 정렬 알고리즘

### 1) 파일 입출력 예시
데이터의 영구 보존을 위해 `FILE*` 포인터를 사용하여 외부 텍스트 파일에 데이터를 쓰고 닫는 기본적인 형식입니다.

```c
#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

typedef struct {
    char name[15];
    int score;
} Student;

int main() {
    Student stds[3] = { {"김철수", 85}, {"이영희", 95}, {"박민수", 90} };
    FILE* fp = fopen("student_data.txt", "w"); // 파일 쓰기 모드 오픈
    
    if (fp != NULL) {
        for (int i = 0; i < 3; i++) {
            fprintf(fp, "%s %d\n", stds[i].name, stds[i].score);
        }
        fclose(fp); // 자원 반환
        printf("파일 저장이 완료되었습니다.\n");
    }
    return 0;
}
```

### 2) 주요 정렬 알고리즘
* **버블 정렬(Bubble Sort)**: 인접한 두 원소를 비교하여 큰 값을 뒤로 밀어내는 방식입니다.
* **선택 정렬(Selection Sort)**: 가장 작은 값을 찾아서 차례대로 맨 앞으로 이동시키는 방식입니다.
* **퀵 정렬(Quick Sort)**: 기준값(Pivot)을 설정하고 이보다 작은 값은 왼쪽, 큰 값은 오른쪽으로 재귀 분할하는 방식입니다.

---

## 5. C언어 코딩 관례 및 에러 처리 (SE 겹침)

* **명명 규칙**: 변수명과 함수명은 주로 `snake_case`를 사용하며, 매크로 상수(`#define`)는 `UPPER_CASE`를 사용합니다.
* **포인터 기호 위치**: 포인터 변수 선언 시 아스터리스크(`*`)는 주로 변수명 바로 앞에 붙이는 방식을 선호합니다. (예: `int *ptr;`)
* **헤더 파일 분리**: 공통으로 사용되는 함수 원형, 구조체 정의, 매크로 상수 등은 확장자가 `.h`인 헤더 파일에 작성하는 것을 권장합니다.
* **에러 처리 방식**: C언어에는 `try-catch` 구문이 없으므로, 함수의 반환값(예: 정상 종료는 `0`, 에러는 `-1` 또는 `NULL`)을 직접 확인하여 예외 처리를 수행하는 방식을 사용합니다.
* **정적/동적 검사 도구**:
  * **clang-format**: 소스코드의 가독성을 위한 포맷터.
  * **cppcheck**: 소스코드 수정을 동반하지 않는 정적 분석 도구.
  * **Valgrind**: 메모리 누수(Memory Leak) 및 오류를 검사하는 도구.
