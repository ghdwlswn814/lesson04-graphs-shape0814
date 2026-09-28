
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
