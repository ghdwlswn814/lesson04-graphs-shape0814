
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    """
    1년간 박스오피스 10위권에 진입한 영화 중
    해당 기간에 개봉한 216편의 데이터를 살펴봅니다.

    영화의 분포와 여러 변수 사이의 관계를 그래프로 알아봅니다.
    """
)

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "happykth/data/main/kobis_movies.csv"
)


# ---------------------------------
# 데이터 불러오기 및 전처리
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 열 이름 양쪽 공백 제거
    df.columns = df.columns.str.strip()

    # 개봉일: 8자리 문자열을 날짜형으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 장르가 여러 개면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미분류")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 장르가 비어 있으면 미분류로 처리
    df["genre"] = df["genre"].replace("", "미분류")

    # 숫자형으로 변환할 열
    numeric_cols = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        ).fillna(0)

    # 영화명 결측치 처리
    df["movieNm"] = df["movieNm"].fillna("영화명 미상")

    return df


# ---------------------------------
# 데이터 로드
# ---------------------------------
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
    st.stop()


if df.empty:
    st.warning("불러온 데이터가 없습니다.")
    st.stop()


# ---------------------------------
# 데이터 개요
# ---------------------------------
st.header("📋 데이터 살펴보기")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 영화 수", f"{len(df):,}편")

with col2:
    st.metric("장르 수", f"{df['genre'].nunique():,}개")

with col3:
    st.metric(
        "분석 기간",
        f"{df['openDt'].min():%Y.%m.%d} ~ "
        f"{df['openDt'].max():%Y.%m.%d}"
        if df["openDt"].notna().any()
        else "날짜 정보 없음"
    )

with st.expander("원본 데이터 확인하기"):
    st.dataframe(df, use_container_width=True)


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================
st.divider()
st.header("그래프 1. 장르별 영화 편수")
st.markdown(
    "영화 216편은 어떤 장르로 구성되어 있을까요?"
)

# 장르별 영화 편수 집계
genre_counts = (
    df.groupby("genre")
    .size()
    .reset_index(name="영화 편수")
    .sort_values("영화 편수", ascending=False)
)

# 비율 계산
genre_counts["비율"] = (
    genre_counts["영화 편수"]
    / genre_counts["영화 편수"].sum()
    * 100
)

# Plotly 도넛 그래프
fig1 = px.pie(
    genre_counts,
    names="genre",
    values="영화 편수",
    hole=0.48,
    title="장르별 영화 편수와 비율",
    custom_data=["비율"],
)

fig1.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate=(
        "<b>장르: %{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{customdata[0]:.1f}%"
        "<extra></extra>"
    ),
)

fig1.update_layout(
    height=550,
    legend_title_text="장르",
    margin=dict(t=80, b=30, l=20, r=20),
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info(
    "전체 영화에서 어떤 장르가 가장 많은 비중을 차지하는지 "
    "확인하고, 장르별 영화 편수와 구성 비율을 비교할 수 있습니다."
)


# ==================================================
# 그래프 추가 예정 구역
# ==================================================
st.divider()
st.header("📊 그래프 2. 분포와 관계")
st.caption(
    "이 구역에 다음 그래프를 추가할 수 있습니다."
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info(
    "추가할 그래프의 분석 목적에 맞춰 설명을 작성합니다."
)

st.divider()
st.header("📊 그래프 3. 변수 사이의 관계")
st.caption(
    "이 구역에 다음 그래프를 추가할 수 있습니다."
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info(
    "추가할 그래프에서 발견한 변수 간 관계나 특징을 작성합니다."
)

# ---------------------------------
# 푸터
# ---------------------------------
st.divider()
st.caption(
    "데이터 출처: KOBIS 영화관입장권통합전산망 "
    "| 분석 대상: 1년간 박스오피스 10위권 진입 영화"
)


# ==================================================
# 그래프 2. 장르별 영화 총 관객 트리맵
# ==================================================
st.divider()

st.header("그래프 2. 장르별 영화 관객 분포")

st.markdown(
    "장르별로 영화를 묶고, 각 영화의 총 관객 규모를 비교합니다."
)

# 트리맵에 사용할 데이터 준비
treemap_df = df.copy()

# 장르와 영화명 결측치 처리
treemap_df["genre"] = (
    treemap_df["genre"]
    .fillna("미분류")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

treemap_df["movieNm"] = (
    treemap_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)

# 총 관객수를 숫자로 변환
treemap_df["total_audi"] = pd.to_numeric(
    treemap_df["total_audi"],
    errors="coerce"
).fillna(0)

# 관객수가 0 이하인 데이터는 트리맵에서 제외
treemap_df = treemap_df[
    treemap_df["total_audi"] > 0
].copy()

# Plotly 트리맵 생성
fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 안에 포함된 영화별 총 관객",
    color="total_audi",
    color_continuous_scale="Blues",
)

# 영화명과 총 관객수를 마우스 오버에 표시
fig2.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>영화명: %{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    ),
)

fig2.update_layout(
    height=750,
    margin=dict(t=70, b=30, l=20, r=20),
    coloraxis_colorbar=dict(
        title="총 관객수"
    ),
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "장르별 관객 규모와 각 장르 안에서 총 관객이 많은 영화 및 "
    "상대적으로 적은 영화를 면적을 통해 비교할 수 있습니다."
)

# ==================================================
# 그래프 3. 총 관객수 히스토그램
# ==================================================
st.divider()

st.header("그래프 3. 영화별 총 관객수 분포")

st.markdown(
    "영화별 총 관객수가 어떤 구간에 많이 분포하는지 살펴봅니다."
)

# 데이터 복사 및 숫자형 변환
hist_df = df.copy()

hist_df["total_audi"] = pd.to_numeric(
    hist_df["total_audi"],
    errors="coerce"
)

hist_df = hist_df.dropna(
    subset=["total_audi"]
)

# 관객수가 0명 초과인 영화만 사용
hist_df = hist_df[
    hist_df["total_audi"] > 0
].copy()

if not hist_df.empty:

    # 가장 관객이 많은 영화
    max_movie = hist_df.loc[
        hist_df["total_audi"].idxmax()
    ]

    max_movie_name = max_movie["movieNm"]
    max_movie_audience = max_movie["total_audi"]

    # 히스토그램
    fig3 = px.histogram(
        hist_df,
        x="total_audi",
        nbins=20,
        title="영화별 총 관객수 히스토그램",
        labels={
            "total_audi": "총 관객수(명)",
            "count": "영화 편수"
        },
        hover_data={
            "total_audi": ":,.0f"
        },
    )

    fig3.update_traces(
        marker_line_color="white",
        marker_line_width=1,
        hovertemplate=(
            "총 관객수 구간: %{x:,.0f}명<br>"
            "영화 편수: %{y}편"
            "<extra></extra>"
        ),
    )

    fig3.update_layout(
        height=550,
        xaxis_title="총 관객수(명)",
        yaxis_title="영화 편수",
        bargap=0.08,
        margin=dict(t=70, b=40, l=30, r=20),
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ---------------------------------
    # 그래프 해석 문구
    # ---------------------------------

    # 가장 많은 영화가 포함된 구간 계산
    counts, bin_edges = pd.cut(
        hist_df["total_audi"],
        bins=20,
        retbins=True,
        include_lowest=True
    )

    bin_counts = counts.value_counts(
        sort=False
    )

    most_common_bin = bin_counts.idxmax()

    lower = most_common_bin.left
    upper = most_common_bin.right

    most_common_count = bin_counts.max()

    st.markdown("#### 💡 이 그래프로 알 수 있는 것")

    st.info(
        f"영화 {len(hist_df):,}편 중 가장 많은 영화가 몰린 구간은 "
        f"{lower:,.0f}명~{upper:,.0f}명이며, "
        f"이 구간에 {most_common_count:,}편이 포함되어 있습니다. "
        f"총 관객이 가장 많은 영화는 "
        f"'{max_movie_name}'으로, "
        f"총 관객은 {max_movie_audience:,.0f}명입니다."
    )

else:
    st.warning("총 관객수 데이터가 없습니다.")

# ==================================================
# 그래프 4. 개봉일 스크린수와 총 관객의 산점도
# ==================================================
st.divider()

st.header("그래프 4. 개봉일 스크린수와 총 관객의 관계")

st.markdown(
    "영화가 개봉일에 얼마나 많은 스크린을 확보했는지와 "
    "최종 총 관객수 사이의 관계를 살펴봅니다."
)

# ---------------------------------
# 산점도 데이터 준비
# ---------------------------------
scatter_df = df.copy()

# 숫자형으로 변환
scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"],
    errors="coerce"
)

scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"],
    errors="coerce"
)

# 필요한 데이터가 있는 행만 사용
scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi", "genre"]
).copy()

# 영화명과 장르 결측치 처리
scatter_df["movieNm"] = (
    scatter_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)

scatter_df["genre"] = (
    scatter_df["genre"]
    .fillna("미분류")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

scatter_df["genre"] = scatter_df["genre"].replace(
    "", "미분류"
)

# 스크린 수와 관객수가 0보다 큰 영화만 사용
scatter_df = scatter_df[
    (scatter_df["first_scrn"] > 0)
    & (scatter_df["total_audi"] > 0)
].copy()


# ---------------------------------
# 산점도 그리기
# ---------------------------------
if not scatter_df.empty:

    fig4 = px.scatter(
        scatter_df,
        x="first_scrn",
        y="total_audi",
        color="genre",
        hover_name="movieNm",
        hover_data={
            "first_scrn": ":,.0f",
            "total_audi": ":,.0f",
            "genre": True,
        },
        labels={
            "first_scrn": "개봉일 스크린수(개)",
            "total_audi": "총 관객수(명)",
            "genre": "장르",
        },
        title="개봉일 스크린수와 총 관객수의 관계",
        opacity=0.75,
    )

    fig4.update_traces(
        marker=dict(
            size=10,
            line=dict(width=0.5, color="white"),
        ),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "장르: %{fullData.name}<br>"
            "개봉일 스크린수: %{x:,.0f}개<br>"
            "총 관객수: %{y:,.0f}명"
            "<extra></extra>"
        ),
    )

    fig4.update_layout(
        height=650,
        xaxis_title="개봉일 스크린수(개)",
        yaxis_title="총 관객수(명)",
        legend_title_text="장르",
        margin=dict(t=70, b=40, l=40, r=20),
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.markdown("#### 💡 이 그래프로 알 수 있는 것")

    st.info(
        "개봉일 스크린수가 많은 영화와 총 관객수가 많은 영화가 "
        "어떤 관계를 보이는지 살펴보고, 장르별로 영화들의 분포를 "
        "비교할 수 있습니다. 다만 스크린수와 총 관객의 관계만으로 "
        "스크린수가 관객 증가의 원인이라고 단정할 수는 없습니다."
    )

else:
    st.warning("산점도를 그릴 수 있는 데이터가 없습니다.")

# ==================================================
# 그래프 5. 장르별 총 관객수 박스플롯
# ==================================================
st.divider()

st.header("그래프 5. 장르별 총 관객수 분포")

st.markdown(
    "영화가 10편 이상인 장르만 골라 "
    "장르별 총 관객수의 분포와 이상치를 비교합니다."
)

# ---------------------------------
# 박스플롯 데이터 준비
# ---------------------------------
box_df = df.copy()

# 장르가 여러 개면 첫 번째 장르만 사용
box_df["genre"] = (
    box_df["genre"]
    .fillna("미분류")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

box_df["genre"] = box_df["genre"].replace(
    "", "미분류"
)

# 영화명 결측치 처리
box_df["movieNm"] = (
    box_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)

# 총 관객수 숫자형 변환
box_df["total_audi"] = pd.to_numeric(
    box_df["total_audi"],
    errors="coerce"
)

# 총 관객수가 없는 행 제거
box_df = box_df.dropna(
    subset=["total_audi"]
)

# 관객수가 0보다 큰 영화만 사용
box_df = box_df[
    box_df["total_audi"] > 0
].copy()

# ---------------------------------
# 영화가 10편 이상인 장르 선택
# ---------------------------------
genre_counts = box_df["genre"].value_counts()

selected_genres = genre_counts[
    genre_counts >= 10
].index.tolist()

box_df = box_df[
    box_df["genre"].isin(selected_genres)
].copy()

# ---------------------------------
# 박스플롯 그리기
# ---------------------------------
if not box_df.empty:

    # 장르별 영화 편수 순서로 표시
    genre_order = (
        box_df["genre"]
        .value_counts()
        .index.tolist()
    )

    fig5 = px.box(
        box_df,
        x="genre",
        y="total_audi",
        color="genre",
        points="outliers",
        hover_name="movieNm",
        category_orders={
            "genre": genre_order
        },
        custom_data=["movieNm"],
        labels={
            "genre": "장르",
            "total_audi": "총 관객수(명)",
        },
        title="영화 10편 이상인 장르의 총 관객수 분포",
    )

    # 이상치 점에 마우스를 올리면 영화명과 관객수 표시
    fig5.update_traces(
        hovertemplate=(
            "<b>영화명: %{customdata[0]}</b><br>"
            "장르: %{x}<br>"
            "총 관객수: %{y:,.0f}명"
            "<extra></extra>"
        ),
        marker=dict(
            size=8,
            opacity=0.8,
        ),
        boxmean=True,
    )

    fig5.update_layout(
        height=650,
        xaxis_title="장르",
        yaxis_title="총 관객수(명)",
        showlegend=False,
        margin=dict(t=70, b=40, l=40, r=20),
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # ---------------------------------
    # 그래프 해석 문구
    # ---------------------------------
    st.markdown("#### 💡 이 그래프로 알 수 있는 것")

    st.info(
        "상자의 가운데 선은 장르별 총 관객수의 중앙값을, "
        "상자의 높이는 가운데 50% 영화의 관객수 범위를 나타냅니다. "
        "수염 밖에 표시된 점은 이상치이며, 마우스를 올리면 "
        "해당 영화명과 총 관객수를 확인할 수 있습니다."
    )

else:
    st.warning(
        "영화가 10편 이상인 장르 중 "
        "박스플롯을 그릴 수 있는 데이터가 없습니다."
    )

# ==================================================
# 그래프 6. 첫 주 관객수를 반영한 버블 그래프
# ==================================================
st.divider()

st.header("그래프 6. 첫 주 관객수와 총 관객의 관계")

st.markdown(
    "그래프 4의 산점도에 첫 주 관객수를 점 크기로 추가했습니다. "
    "개봉일 스크린수, 첫 주 관객수, 총 관객수의 관계를 "
    "함께 살펴봅니다."
)

# ---------------------------------
# 버블 그래프 데이터 준비
# ---------------------------------
bubble_df = df.copy()

# 숫자형으로 변환
numeric_cols = [
    "first_scrn",
    "first_week_audi",
    "total_audi"
]

for col in numeric_cols:
    bubble_df[col] = pd.to_numeric(
        bubble_df[col],
        errors="coerce"
    )

# 필요한 데이터가 있는 행만 사용
bubble_df = bubble_df.dropna(
    subset=[
        "first_scrn",
        "first_week_audi",
        "total_audi"
    ]
).copy()

# 영화명 결측치 처리
bubble_df["movieNm"] = (
    bubble_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)

# 장르가 여러 개면 첫 번째 장르만 사용
bubble_df["genre"] = (
    bubble_df["genre"]
    .fillna("미분류")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

bubble_df["genre"] = bubble_df["genre"].replace(
    "", "미분류"
)

# 음수 또는 0인 값 제외
bubble_df = bubble_df[
    (bubble_df["first_scrn"] > 0)
    & (bubble_df["first_week_audi"] > 0)
    & (bubble_df["total_audi"] > 0)
].copy()


# ---------------------------------
# 버블 그래프 그리기
# ---------------------------------
if not bubble_df.empty:

    fig6 = px.scatter(
        bubble_df,
        x="first_scrn",
        y="total_audi",
        size="first_week_audi",
        color="genre",
        hover_name="movieNm",
        hover_data={
            "first_scrn": ":,.0f",
            "first_week_audi": ":,.0f",
            "total_audi": ":,.0f",
            "genre": True,
        },
        size_max=55,
        opacity=0.65,
        labels={
            "first_scrn": "개봉일 스크린수(개)",
            "total_audi": "총 관객수(명)",
            "first_week_audi": "첫 주 관객수(명)",
            "genre": "장르",
        },
        title="개봉일 스크린수 · 첫 주 관객수 · 총 관객수",
    )

    fig6.update_traces(
        marker=dict(
            sizemode="area",
            line=dict(
                width=0.5,
                color="white"
            ),
        ),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "장르: %{fullData.name}<br>"
            "개봉일 스크린수: %{x:,.0f}개<br>"
            "총 관객수: %{y:,.0f}명<br>"
            "첫 주 관객수: %{marker.size:,.0f}명"
            "<extra></extra>"
        ),
    )

    fig6.update_layout(
        height=700,
        xaxis_title="개봉일 스크린수(개)",
        yaxis_title="총 관객수(명)",
        legend_title_text="장르",
        margin=dict(t=70, b=40, l=40, r=20),
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    # ---------------------------------
    # 그래프 해석 문구
    # ---------------------------------
    st.markdown("#### 💡 이 그래프로 알 수 있는 것")

    st.info(
        "점의 가로 위치는 개봉일 스크린수, 세로 위치는 총 관객수, "
        "크기는 첫 주 관객수를 나타냅니다. "
        "이를 통해 첫 주 관객수가 많았던 영화가 최종적으로 "
        "얼마나 많은 관객을 모았는지 장르별로 비교할 수 있습니다."
    )

else:
    st.warning(
        "버블 그래프를 그릴 수 있는 데이터가 없습니다."
    )

# ==================================================
# 그래프 7. 제작 국가별 장르 선버스트 그래프
# ==================================================
st.divider()

st.header("그래프 7. 제작 국가별 장르 분포")

st.markdown(
    "제작 국가에서 장르로 내려가는 계층 구조를 통해 "
    "국가별 영화 구성과 장르 분포를 살펴봅니다."
)

# ---------------------------------
# 선버스트 데이터 준비
# ---------------------------------
sunburst_df = df.copy()

# 제작 국가 결측치 처리
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("미분류")
    .astype(str)
    .str.strip()
)

sunburst_df["nation"] = sunburst_df["nation"].replace(
    "", "미분류"
)

# 장르가 여러 개면 첫 번째 장르만 사용
sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("미분류")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

sunburst_df["genre"] = sunburst_df["genre"].replace(
    "", "미분류"
)

# 영화명 결측치 처리
sunburst_df["movieNm"] = (
    sunburst_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)

# 국가별 장르별 영화 편수 집계
sunburst_counts = (
    sunburst_df
    .groupby(["nation", "genre"])
    .size()
    .reset_index(name="영화 편수")
)

# ---------------------------------
# 선버스트 그래프 그리기
# ---------------------------------
if not sunburst_counts.empty:

    fig7 = px.sunburst(
        sunburst_counts,
        path=["nation", "genre"],
        values="영화 편수",
        title="제작 국가 → 장르별 영화 편수",
        color="nation",
        hover_data={
            "영화 편수": True
        },
    )

    fig7.update_traces(
        textinfo="label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "영화 편수: %{value}편"
            "<extra></extra>"
        ),
        insidetextorientation="radial",
    )

    fig7.update_layout(
        height=750,
        margin=dict(t=70, b=30, l=20, r=20),
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

    # ---------------------------------
    # 그래프 해석 문구
    # ---------------------------------
    st.markdown("#### 💡 이 그래프로 알 수 있는 것")

    st.info(
        "제작 국가별 영화 편수와 각 국가에서 많이 등장하는 장르를 "
        "비교할 수 있으며, 칸의 크기를 통해 전체 영화에서 "
        "각 국가와 장르가 차지하는 비중을 확인할 수 있습니다."
    )

else:
    st.warning(
        "선버스트 그래프를 그릴 수 있는 데이터가 없습니다."
    )

# ==================================================
# 그래프 8. 첫 주에 관객을 많이 모은 영화가 최종 흥행에도 성공했는가
# ==================================================
st.divider()

question8 = "첫 주에 관객을 많이 모은 영화가 최종 흥행에도 성공했는가"

st.header("그래프 8. " + question8)

# ---------------------------------
# 데이터 준비
# ---------------------------------
scatter8_df = df.copy()

# 숫자형으로 변환
scatter8_df["days_in_top10"] = pd.to_numeric(
    scatter8_df["days_in_top10"],
    errors="coerce"
)

scatter8_df["total_audi"] = pd.to_numeric(
    scatter8_df["total_audi"],
    errors="coerce"
)

# 영화명 결측치 처리
scatter8_df["movieNm"] = (
    scatter8_df["movieNm"]
    .fillna("영화명 미상")
    .astype(str)
)

# 필요한 데이터가 있는 행만 사용
scatter8_df = scatter8_df.dropna(
    subset=["days_in_top10", "total_audi"]
).copy()

# 유효한 데이터만 사용
scatter8_df = scatter8_df[
    (scatter8_df["days_in_top10"] > 0)
    & (scatter8_df["total_audi"] > 0)
].copy()

# ---------------------------------
# 산점도 그리기
# ---------------------------------
if not scatter8_df.empty:

    fig8 = px.scatter(
        scatter8_df,
        x="days_in_top10",
        y="total_audi",
        hover_name="movieNm",
        hover_data={
            "days_in_top10": ":,.0f",
            "total_audi": ":,.0f",
        },
        labels={
            "days_in_top10": "10위권에 머문 날수(일)",
            "total_audi": "총 관객수(명)",
        },
        title=question8,
        opacity=0.75,
    )

    fig8.update_traces(
        marker=dict(
            size=10,
            line=dict(
                width=0.5,
                color="white"
            ),
        ),
        hovertemplate=(
            "<b>영화명: %{hovertext}</b><br>"
            "10위권에 머문 날수: %{x:,.0f}일<br>"
            "총 관객수: %{y:,.0f}명"
            "<extra></extra>"
        ),
    )

    fig8.update_layout(
        height=650,
        xaxis_title="10위권에 머문 날수(일)",
        yaxis_title="총 관객수(명)",
        margin=dict(t=70, b=40, l=40, r=20),
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )

    # ---------------------------------
    # 그래프 해석 문구
    # ---------------------------------
    st.markdown("#### 💡 이 그래프로 알 수 있는 것")

    st.info(
        "점 하나는 영화 한 편을 나타냅니다. "
        "오른쪽 위로 점들이 모이는 경향이 있다면 "
        "10위권에 오래 머문 영화일수록 총 관객수가 많은 "
        "경향이 있음을 살펴볼 수 있습니다. "
        "다만 이 그래프는 첫 주 관객수가 아닌 10위권 체류 일수와 "
        "총 관객수의 관계를 보여 줍니다."
    )

else:
    st.warning(
        "산점도를 그릴 수 있는 데이터가 없습니다."
    )

# --------------------------------------------------
# 그래프 8. 상위 10% 영화의 관객 비중 (파레토 차트)
# --------------------------------------------------

st.divider()

question8 = "전체 관객 중 상위 10% 영화가 차지하는 비중은 얼마나 되는가"

st.header("그래프 8. " + question8)

# 필요한 데이터 정리
pareto_df = df[["movieNm", "days_in_top10", "total_audi"]].copy()

pareto_df["days_in_top10"] = pd.to_numeric(
    pareto_df["days_in_top10"], errors="coerce"
)
pareto_df["total_audi"] = pd.to_numeric(
    pareto_df["total_audi"], errors="coerce"
)

pareto_df = pareto_df.dropna(
    subset=["movieNm", "days_in_top10", "total_audi"]
)

pareto_df = pareto_df[
    (pareto_df["days_in_top10"] > 0) &
    (pareto_df["total_audi"] > 0)
]

# 총 관객 수가 많은 순서로 정렬
pareto_df = pareto_df.sort_values(
    "total_audi", ascending=False
).reset_index(drop=True)

# 전체 관객 수
total_audience = pareto_df["total_audi"].sum()

# 상위 10% 영화 수 (최소 1편)
top_10_count = max(1, int(len(pareto_df) * 0.1))

# 상위 10% 영화 데이터
top_10_df = pareto_df.head(top_10_count)

# 상위 10% 영화의 관객 비중
top_10_audience = top_10_df["total_audi"].sum()
top_10_ratio = top_10_audience / total_audience * 100

# 누적 관객 비중 계산
pareto_df["누적관객비중"] = (
    pareto_df["total_audi"].cumsum()
    / total_audience * 100
)

# 상위 10% 영화 관객 비중 요약
col1, col2, col3 = st.columns(3)

col1.metric(
    "전체 영화 수",
    f"{len(pareto_df):,}편"
)

col2.metric(
    "상위 10% 영화 수",
    f"{top_10_count:,}편"
)

col3.metric(
    "상위 10% 영화의 관객 비중",
    f"{top_10_ratio:.1f}%"
)

# 파레토 차트
import plotly.graph_objects as go

fig8 = go.Figure()

# 영화별 관객 수 산점도
fig8.add_trace(
    go.Scatter(
        x=pareto_df["days_in_top10"],
        y=pareto_df["total_audi"],
        mode="markers",
        name="영화별 총 관객",
        text=pareto_df["movieNm"],
        customdata=pareto_df[["누적관객비중"]],
        hovertemplate=(
            "영화명: %{text}<br>"
            "10위권 체류 일수: %{x}일<br>"
            "총 관객 수: %{y:,.0f}명<br>"
            "누적 관객 비중: %{customdata[0]:.1f}%"
            "<extra></extra>"
        )
    )
)

fig8.update_layout(
    title=question8,
    xaxis_title="10위권에 머문 날수",
    yaxis_title="총 관객 수 (명)",
    yaxis=dict(tickformat=","),
    hovermode="closest",
    height=600
)

st.plotly_chart(fig8, use_container_width=True)

st.caption(
    "이 그래프는 영화별 10위권 체류 일수와 총 관객 수의 관계를 보여 줍니다. "
    "상위 10% 영화의 관객 비중은 전체 영화의 총 관객 수 중 "
    "관객 수 기준 상위 10% 영화들이 차지하는 비율입니다."
)

st.info(
    f"전체 {len(pareto_df)}편 중 관객 수 상위 "
    f"{top_10_count}편({top_10_count / len(pareto_df) * 100:.1f}%)이 "
    f"전체 관객의 {top_10_ratio:.1f}%를 차지합니다."
)
