import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: '|' 구분 기호가 있는 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

# ---------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")

# 장르별 빈도수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 비율",
)

# 마우스 호버 시 편수와 비율이 나오도록 설정
fig_donut.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}",
)

st.plotly_chart(fig_donut, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "개봉한 주요 영화 중 특정 장르가 차지하는 비중과 다수 편성된 주요 장르를 한눈에 파악할 수 있습니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 2. 장르별 영화 총 관객수 (트리맵 그래프)
# ---------------------------------------------------------
st.header("2. 장르 및 영화별 총 관객수 분포")

# Plotly 트리맵 생성 (장르 > 영화명 계층 구조)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 (칸 크기: 총 관객수)",
    hover_data={"total_audi": ":,d"},
)

# 마우스 호버 시 영화명과 총 관객수가 보이도록 설정
fig_treemap.update_traces(
    hovertemplate="<b>영화명:</b> %{label}<br><b>총 관객수:</b> %{value:,}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "장르별 전체 관객수 규모와 함께 각 장르 내에서 어떤 영화가 총 관객수 흥행을 주도했는지 직관적으로 비교할 수 있습니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 3. 총 관객수 히스토그램
# ---------------------------------------------------------
st.header("3. 총 관객수 분포 (히스토그램)")

# Plotly 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객수 분포",
    labels={"total_audi": "총 관객수(명)"},
)

# 마우스 호버 및 레이아웃 설정
fig_hist.update_traces(
    hovertemplate="<b>관객수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
)
fig_hist.update_layout(yaxis_title="영화 수 (편)")

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 관객 수가 많은 영화 정보 추출
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# 데이터 기반 분석 문구 생성
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화가 총 관객수 **100만 명 미만 구간**에 집중되어 있으며, "
    f"가장 관객 수가 많은 영화는 **'{top_movie_name}'**(약 {top_movie_audi:,}명)입니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객수 (산점도)
# ---------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

# Plotly 산점도 생성
fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객수(명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,d",
        "total_audi": ":,d",
    },
)

# 마우스 호버 포맷 지정
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "개봉일에 확보한 스크린수가 많을수록 총 관객수도 증가하는 양의 상관관계를 보이며, 장르별 스크린 확보 수준 및 흥행 규모 차이를 확인할 수 있습니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 5. 주요 장르별 총 관객수 분포 (상자 그림)
# ---------------------------------------------------------
st.header("5. 주요 장르별 총 관객수 분포 (박스플롯)")

# 영화 수 10편 이상인 장르만 필터링
genre_counts_series = df["genre"].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_top_genres = df[df["genre"].isin(top_genres)]

# Plotly 상자 그림 생성
fig_box = px.box(
    df_top_genres,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",  # 이상치(상자 밖 점) 표시
    hover_name="movieNm",  # 이상치 점 호버 시 영화명 표시
    title="영화 수 10편 이상 주요 장르의 총 관객수 분포",
    labels={"genre": "장르", "total_audi": "총 관객수(명)"},
    hover_data={"total_audi": ":,d"},
)

# 마우스 호버 시 영화명과 총 관객수가 깔끔하게 표시되도록 설정
fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_box, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "10편 이상 제작된 주요 장르 간 관객수 중앙값과 변동성을 비교할 수 있으며, 상자 밖의 대형 흥행 성공작(이상치)의 존재 유무를 한눈에 파악할 수 있습니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 6. 개봉일 스크린수 vs 총 관객수 (버블 차트)
# ---------------------------------------------------------
st.header("6. 스크린수, 총 관객수, 첫 주 관객수의 종합 관계 (버블 차트)")

# Plotly 버블 차트 생성
fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,
    title="개봉일 스크린수 vs 총 관객수 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객수(명)",
        "first_week_audi": "개봉 첫 주 관객수(명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,d",
        "total_audi": ":,d",
        "first_week_audi": ":,d",
    },
)

# 마우스 호버 포맷 지정
fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>개봉 첫 주 관객수: %{customdata[2]:,}명<extra></extra>"
)

st.plotly_chart(fig_bubble, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "스크린수와 총 관객수의 관계에 더해, 원의 크기를 통해 초반 기선 제압(개봉 첫 주 흥행)에 성공한 영화가 최종 총 관객수에도 결정적인 영향을 주는지 입체적으로 파악할 수 있습니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ---------------------------------------------------------
st.header("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트 차트)")

# Plotly 선버스트 차트 생성 (국가 > 장르 계층 구조)
fig_sunburst = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가 - 장르 계층별 영화 편수 (칸 크기: 영화 편수)",
)

# 마우스 호버 시 구분 항목 및 영화 편수/비율 표시
fig_sunburst.update_traces(
    hovertemplate="<b>분류:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>하위비율:</b> %{percentParent:.1%}<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "각 제작 국가별로 어떤 장르의 영화가 주를 이루는지 계층적으로 살펴볼 수 있으며, 국가 간 장르 구성의 차이를 한눈에 비교할 수 있습니다."
)
st.markdown("---")


# ---------------------------------------------------------
# 8. 10위권 체류 기간과 총 관객수의 관계 (산점도)
# ---------------------------------------------------------
st.header("8. 10위권에 오래 머문 영화는 총 관객도 많은가")

# Plotly 산점도 생성
fig_scatter_days = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "10위권에 머문 날수(일)",
        "total_audi": "총 관객수(명)",
        "genre": "장르",
    },
    hover_data={
        "days_in_top10": ":,d",
        "total_audi": ":,d",
    },
)

# 마우스 호버 포맷 지정
fig_scatter_days.update_traces(
    hovertemplate="<b>%{hovertext}</b><br><br>10위권 머문 날수: %{x:,}일<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_scatter_days, use_container_width=True)

# 시각화 해석 구역 구분
st.markdown("---")
st.subheader("💡 이 그래프로 알 수 있는 것")
st.info(
    "박스오피스 TOP 10 진입 일수가 긴 영화일수록 대체로 총 관객수도 많은 강력한 양의 상관관계를 보여주며, 오랜 롱런 흥행이 최종 흥행 성과에 매우 중요한 요소임을 알 수 있습니다."
)
st.markdown("---")
