---
layout: post
date: 2026-06-11
title: 02. C# 클래스, WinForm 및 장비제어 (WinForms & Equipment Control)
author: Voliti
category_name: csharp
---

## 1. 내장 유틸리티 클래스 및 람다 식

C#에서 제공하는 대표적인 내장 클래스의 특징과 람다 식의 활용법입니다.

### 1) Random, List, Math
* **`Random`**: 정수 및 실수 범위의 난수를 반환합니다. (`random.Next(10, 100)`)
* **`List<T>`**: 크기가 유동적으로 변하는 동적 배열 클래스입니다.
  * 람다 식(`=>`)을 사용하여 다수의 항목을 필터링하여 지울 수 있습니다. (예: `list.RemoveAll(n => n < 50);`)
* **`Math`**: 정적 클래스로서 `Abs`(절대값), `Ceiling`(올림), `Floor`(내림), `Round`(반올림), `Max`/`Min` 등의 유틸리티 연산을 지원합니다.

---

## 2. 클래스 정의, 속성(Property) 및 값/참조 복사

### 1) 게터(Getter)와 세터(Setter) 속성
C#은 단순한 캡슐화 변수 보호를 위해 길게 작성하는 getter/setter 메서드 대신 단일 **속성(Property)** 구문을 사용하여 간결하게 표현합니다.
* **자동 구현 속성**: `public string Name { get; set; }`
* **백킹 필드(Backing Field) 활용**: 속성에 추가적인 비즈니스 로직(예: Null 방지 등)을 녹여낼 수 있습니다.

```csharp
public class Student
{
    private string addr; // 백킹 필드

    public string Addr
    {
        get { return addr ?? "주소 미설정"; }
        set { if (value != null) addr = value; }
    }
}
```

### 2) 값 복사(Value Copy) vs 참조 복사(Reference Copy)
* **값 타입(struct, int 등)**: 값을 완전히 복사하므로 복사본을 함수 내에서 수정해도 원본에 영향이 없습니다.
* **참조 타입(class, array 등)**: 힙 영역의 주소 포인터를 전달하므로, 함수 내부에서 멤버 변수를 변경하면 원본 객체의 데이터도 즉시 변동됩니다.

---

## 3. Windows Forms (WinForm) 이벤트 기반 프로그래밍

WinForm은 C#에서 데스크톱 GUI 프로그램(특히 산업용 장비 MMI 화면)을 작성할 때 널리 쓰이는 프레임워크입니다.

### 1) 주요 기법 및 이벤트 처리
* **이벤트 동적 연결**: `button1.Click += Button1_Click;` 처럼 대리자(Delegate) 기반으로 이벤트 핸들러를 런타임에 동적으로 매핑합니다.
* **sender 객체**: 이벤트를 유발한 원본 컨트롤(Control)을 참조하며 캐스팅하여 사용합니다. (`Button self = (Button)sender;`)
* **FormClosed 이벤트**: 창이 완전히 닫힌 직후 발생하여 자원 해제, 최종 로그 기록(`System.IO.File.AppendAllText`) 등을 수행합니다.
* **Timer 컨트롤**: 백그라운드 스레드 없이 매 Tick 주기마다 UI 컴포넌트의 시간이나 센서 상태를 실시간 업데이트할 때 사용합니다.

```csharp
private void timer1_Tick(object sender, EventArgs e)
{
    elapsedTime++;
    textBox2.Text = $"{elapsedTime}초 경과";
}
```

---

## 4. 장비 제어 및 반도체 장비 실습 (SCT & EtherCAT)

공장 자동화 및 반도체 공정 장비에서 사용하는 하드웨어 인터페이스 제어 내용입니다.

### 1) EtherCAT 산업용 통신
* **EtherCAT (Ethernet for Control Automation Technology)**: 고성능 실시간 분산 제어를 위한 산업용 이더넷 네트워크 프로토콜입니다.
* **특징**: TCP/IP 7계층 오버헤드 없이 하드웨어 레벨(Layer 2)에서 MAC/IP 주소 관리 없이 직접 프레임을 전송하므로 실시간 클럭 동기화 및 초고속 DMA가 가능합니다.

### 2) SCT(Semiconductor Control Trainer) API 연결 흐름
반도체 이송 모의 장비를 제어하기 위해 윈도우 Dynamic Link Library 파일(`IEG3264_DLL.dll`)을 참조하여 C# 클래스에서 호출하는 시퀀스입니다:
1. **마스터 연결**: `DriveConnect()` 호출을 통해 EtherCAT 네트워크 개시.
2. **센서 입력 로드**: `xChannelRead()` 함수로 실시간 센서 및 스위치 입력 데이터 수신.
3. **액추에이터 출력 구동**: `xChannelWrite(byte[] data)` 함수로 장비의 실린더, 모터, 밸브 등에 전기 신호 전송.
4. **마스터 해제**: `close()` 호출로 통신 자원 정리.

### 3) 디지털 I/O 결선 주소 예시 (반도체 8대 공정 프로젝트 연계)
* **입력 주소**: P003 (비상정지 스위치 EMG), P005 (메인 압력 센서), P006~011 (도어 실린더 상승/하강 감지), P014 (웨이퍼 진공 이젝터 압력 센서)
* **출력 주소**: P100~102 (적/황/녹 타워램프), P104~111 (각 공정 챔버 도어 솔레노이드 밸브), P114 (웨이퍼 진공 흡기 솔레노이드)

---

## 5. C# 비동기 및 예외 처리 (SE 겹침)

* **비동기 프로그래밍 (async/await)**: `async` 키워드로 선언된 메서드는 내부에서 `await` 비동기 태스크를 사용합니다. 이는 무거운 I/O 작업(예: DB 연동, 대량의 센서 주기적 폴링 등)을 수행할 때 UI 스레드가 블로킹되어 프로그램이 멈추는(Not Responding) 현상을 방지합니다.
* **예외 처리 구문**: C#은 `try - catch - finally` 구문과 직접 예외를 던지는 `throw new Exception("메시지");`를 사용하여 런타임 오류가 전체 시스템 정지로 전이되는 것을 차단합니다.
