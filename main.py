# ==================================================
# 그래프 2. 장르별 영화 트리맵
# ==================================================
st.divider()
st.header("그래프 2. 장르별 영화 관객 분포")

st.markdown(
    "장르 안에 어떤 영화들이 포함되어 있고, "
    "각 영화의 총 관객은 얼마나 되는지 살펴봅니다."
)

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵",
)

fig2.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
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
    "장르별 전체 관객 규모와 각 장르 안에서 "
    "총 관객이 많은 영화를 비교할 수 있습니다."
)
