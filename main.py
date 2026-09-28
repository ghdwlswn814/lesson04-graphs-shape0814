
# ==================================================
# 그래프 2. 장르별 영화 트리맵
# ==================================================
st.divider()
st.header("그래프 2. 장르별 영화 관객 분포")
st.markdown(
    "장르 안에 어떤 영화들이 포함되어 있고, "
    "각 영화의 총 관객은 얼마나 되는지 살펴봅니다."
)

# 영화별 총 관객을 기준으로 트리맵 생성
fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵",
    custom_data=["total_audi"],
)

# 마우스를 올렸을 때 영화명과 총 관객 표시
fig2.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{customdata[0]:,.0f}명"
        "<extra></extra>"
    ),
)

fig2.update_layout(
    height=700,
    margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르별 전체 관객 규모와 장르 안에서 어떤 영화가 "
    "총 관객의 큰 비중을 차지하는지 비교할 수 있습니다."
)
