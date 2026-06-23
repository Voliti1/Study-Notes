---
layout: post
date: 2026-06-04
title: 17. 고급 시각화 및 지리 정보 맵 구현 (Seaborn & Folium)
author: Voliti
category_name: python
subcategory: bigdata
---

## 1. Seaborn 고급 데이터 시각화

Seaborn 라이브러리는 Matplotlib을 기반으로 훨씬 세련된 그래픽 스타일 테마와 복합적인 가독성 차트를 한 줄의 코드로 구현하도록 설계되었습니다.

### 1) 테마 및 팔레트 설정
* `sns.set_theme(style="whitegrid", rc={"figure.figsize": (5, 5)})`: 전체 그래프 캔버스의 뒷배경 격자 격자무늬 및 크기를 조정합니다.
* `sns.set_palette('hls', 4)`: 통일된 하모니 컬러 조합을 주입합니다.

### 2) 고급 차트 유형들
* **sns.barplot**: 기본 평균값 연산뿐 아니라 에러선(신뢰구간, CI)을 차트에 기둥형태로 자동 표시합니다. (`ci=None`으로 소거 가능)
* **sns.boxplot**: 카테고리별 연속 데이터를 한눈에 사분위 분포로 시각화합니다.
* **sns.scatterplot (버블 차트)**: 산점도 위에 점의 색상(`hue`)뿐 아니라 점의 지름 크기(`size`)까지 변수 크기에 연동시켜 다차원 표현을 구성합니다.
* **mosaic (모자이크 플롯)**: 범주형 변수들 간의 다중 비율을 사각형 면적 면적으로 시각화하는 방법입니다. (입력 데이터가 반드시 범주형 범주형이어야 정상 렌더링됩니다.)
* **sns.heatmap (히트맵)**: 2차원 매트릭스 데이터를 색상 테이블(온도 지도)로 표현하여 데이터의 밀도를 효과적으로 검출합니다.

```python
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 피벗을 통해 히트맵용 매트릭스 구축
df_pivot = flights.pivot_table(index="month", columns="year", values="passengers", aggfunc="mean")

sns.set_theme(rc={'figure.figsize': (8, 7)})
sns.heatmap(df_pivot, annot=True, fmt="d") // 정수 텍스트 표기
plt.show()
```

---

## 2. Folium 지리 정보 시각화 및 지오코딩

위도와 경도 좌표값을 기반으로 실제 웹 브라우저 지도 위에 데이터를 플로팅하는 기법입니다.

### 1) geokakao 및 folium 연동
* **`convert_address_to_coordinates`**: 텍스트 형태의 주소를 받아 카카오 API를 사용해 위도와 경도 실수값 좌표쌍으로 치환해주는 라이브러리입니다.
* **`folium.Map`**: 지도의 중심 위치와 최초 확대 비율(`zoom_start`)을 설정합니다.
* **`folium.Marker`**: 마커 객체를 생성해 지도 위에 삽입하며, 마커의 색상, 형태 및 팝업 텍스트를 기입할 수 있습니다.

```python
import folium
import geokakao as gk
import displayMap as dm // 브라우저 자동 오픈용 모듈

# 주소의 좌표 변환
loc = gk.convert_address_to_coordinates('경기 화성시 동탄대로시범길 20')

# 지도 선언 및 마커 배치
map_obj = folium.Map(location=loc, zoom_start=18)
folium.Marker(
    location=loc,
    popup="우리 집",
    icon=folium.Icon(color="red", icon="home")
).add_to(map_obj)

# 지도 html 저장 및 새 브라우저 탭 오픈
dm.showMap(map_obj)
```
