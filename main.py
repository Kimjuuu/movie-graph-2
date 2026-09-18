import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 문자열 접근자(.str)를 직접 연결 사용하여 Python 3.14 호환성 확보
    df["primary_genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    return df


df = load_data()

# ---------------------------------------------------------
# Section 1: 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.markdown("---")
st.header("1. 장르별 영화 편수 분포")

genre_counts = df["primary_genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.4,
    title="장르별 영화 비율 및 편수",
)

fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 개봉한 영화 중 어떤 장르가 가장 높은 비중을 차지하는지 한눈에 파악할 수 있으며, 특정 장르에 편중된 시장 경향성을 도넛 비율로 확인할 수 있습니다."
)

# ---------------------------------------------------------
# Section 2: 장르 및 영화별 총 관객수 분포 (트리맵)
# ---------------------------------------------------------
st.markdown("---")
st.header("2. 장르 및 영화별 총 관객수 분포")

# 고유한 경로 설정을 위해 movieCd를 함께 포함하여 계층 충돌(ValueError) 방지
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "primary_genre", "movieNm", "movieCd"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 트리맵",
    color="primary_genre",
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명",
    root_color="lightgrey",
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 장르 전체의 총 관객 규모뿐만 아니라, 특정 장르 내에서 흥행을 주도한 대표 영화와 관객수의 기여도를 면적의 크기로 한눈에 비교할 수 있습니다."
)

# ---------------------------------------------------------
# Section 3: 총 관객수 분포 (히스토그램)
# ---------------------------------------------------------
st.markdown("---")
st.header("3. 총 관객수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객수 분포 히스토그램",
    labels={"total_audi": "총 관객수 (명)"},
)

fig3.update_traces(
    hovertemplate="<b>관객수 구간: %{x}</b><br>영화 수: %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 관객수가 적은 하위 구간(약 100만 명 미만 구간)에 집중되어 롱테일 형태의 비대칭 분포를 보입니다. "
    f"이 중 가장 많은 관객을 동원한 최고 흥행 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)입니다."
)

# ---------------------------------------------------------
# Section 4: 개봉일 스크린수와 총 관객수의 관계 (산점도)
# ---------------------------------------------------------
st.markdown("---")
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="primary_genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수 산점도",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객수 (명)",
        "primary_genre": "대표 장르",
    },
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 개봉 첫날 확보한 스크린수가 많을수록 대체로 최종 관객수도 높은 양의 상관관계를 보이며, 장르별 스크린 확보 수준 및 흥행 규모 차이를 비교해 볼 수 있습니다."
)

# ---------------------------------------------------------
# Section 5: 주요 장르별 총 관객수 분포 (박스플롯)
# ---------------------------------------------------------
st.markdown("---")
st.header("5. 주요 장르별 총 관객수 분포 (영화 10편 이상 장르)")

genre_counts_series = df["primary_genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df["primary_genre"].isin(major_genres)]

fig5 = px.box(
    df_filtered,
    x="primary_genre",
    y="total_audi",
    color="primary_genre",
    hover_name="movieNm",
    points="outliers",
    title="영화 10편 이상 장르별 총 관객수 박스플롯",
    labels={
        "primary_genre": "장르",
        "total_audi": "총 관객수 (명)",
    },
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객수의 중간값과 편차를 비교할 수 있으며, 박스 범위 바깥의 아웃라이어 점을 통해 장르 평균을 뛰어넘는 대형 흥행작 유무를 쉽게 식별할 수 있습니다."
)

# ---------------------------------------------------------
# Section 6: 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)
# ---------------------------------------------------------
st.markdown("---")
st.header("6. 개봉일 스크린수 · 총 관객수 · 첫 주 관객수의 관계 (버블 차트)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="primary_genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린수 vs 총 관객수 (점 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객수 (명)",
        "first_week_audi": "첫 주 관객수",
        "primary_genre": "대표 장르",
    },
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<br>첫 주 관객수: %{marker.size:,}명"
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 초기 스크린 확보량(X축)과 최종 흥행(Y축)뿐만 아니라 버블 크기(첫 주 관객수)를 함께 파악함으로써, 초반 입소문이나 개봉 첫 주 흥행 에너지가 최종 관객수 선착에 얼마나 결정적이었는지 3차원적 맥락으로 해석할 수 있습니다."
)

# ---------------------------------------------------------
# Section 7: 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ---------------------------------------------------------
st.markdown("---")
st.header("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

fig7 = px.sunburst(
    df,
    path=["nation", "primary_genre"],
    title="제작 국가 및 장르별 영화 편수 선버스트",
    color="nation",
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}"
)

st.plotly_chart(fig7, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 영화를 제작 국가별로 계층화하여 각 국가 내에서 어떤 장르가 다양하게 제작 및 수입되어 개봉했는지 장르별 수량 비중을 원형 다단계 구조로 확인할 수 있습니다."
)

# ---------------------------------------------------------
# Section 8: 순위권 유지 기간과 총 관객수의 관계 (산점도)
# ---------------------------------------------------------
st.markdown("---")
st.header("8. 3위권 유지 기간과 총 관객수의 관계")

fig8 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="primary_genre",
    hover_name="movieNm",
    title="3위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "3위권에 머문 날수 (일)",
        "total_audi": "총 관객수 (명)",
        "primary_genre": "대표 장르",
    },
)

fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>3위권 머문 날수: %{x}일<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig8, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 박스오피스 상위권(10위권)에 롱런하며 오래 머문 일수가 길수록 총 관객수도 비례하여 커지는 뚜렷한 양의 상관관계를 나타냅니다."
)
