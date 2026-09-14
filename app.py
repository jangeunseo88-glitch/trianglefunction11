import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="인터랙티브 삼각함수 교실",
    page_icon="📐",
    layout="wide"
)

# 레이아웃 간격 최적화 CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📐 한 눈에 이해하는 인터랙티브 삼각함수")
st.caption("20년차 수학 교사의 시각화 노하우로 만든 직관적인 sin, cos, tan 삼각함수 탐구실")

# 사이드바 모드 선택
st.sidebar.header("🕹️ 학습 모드 선택")
mode = st.sidebar.radio(
    "원하는 학습 모드를 선택하세요",
    [
        "1. 단위원과 삼각함수 (sin, cos, tan)",
        "2. 🎛️ 함수 변형 탐구 (y = a · fn(bx + c) + d)",
        "3. 🎢 롤러코스터 물리 트랙 설계"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: 슬라이더를 움직이면 그래프가 **실시간**으로 동기화되어 즉시 변경됩니다.")

# =========================================================
# 모드 1: 단위원과 삼각함수 (sin, cos, tan)
# =========================================================
if mode == "1. 단위원과 삼각함수 (sin, cos, tan)":
    st.header("1. 단위원의 움직임과 삼각함수의 원리")
    st.write("단위원 상의 점이 회전할 때, **$y$좌표는 $\sin$**, **$x$좌표는 $\cos$**, **접선의 높이는 $\tan$**가 됩니다.")

    # 각도 및 함수 선택 컨트롤러
    c1, c2 = st.columns([2, 1])
    with c1:
        angle_deg = st.slider("각도 θ (도)", 0, 360, 45, step=1)
    with c2:
        func_type = st.selectbox("관찰할 함수 선택", ["sin (사인)", "cos (코사인)", "tan (탄젠트)"])

    angle_rad = np.radians(angle_deg)
    x_val, y_val = np.cos(angle_rad), np.sin(angle_rad)

    # 2열 시각화 레이아웃
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("단위원 (Unit Circle)")
        fig_circle = go.Figure()

        # 1. 단위원 테두리
        t_circle = np.linspace(0, 2*np.pi, 200)
        fig_circle.add_trace(go.Scatter(x=np.cos(t_circle), y=np.sin(t_circle), mode='lines', name='단위원', line=dict(color='lightgray', dash='dash')))

        # 2. X, Y 축
        fig_circle.add_trace(go.Scatter(x=[-2, 2], y=[0, 0], mode='lines', line=dict(color='#E0E0E0'), showlegend=False))
        fig_circle.add_trace(go.Scatter(x=[0, 0], y=[-2, 2], mode='lines', line=dict(color='#E0E0E0'), showlegend=False))

        # 3. 동경 (Radius Vector)
        fig_circle.add_trace(go.Scatter(x=[0, x_val], y=[0, y_val], mode='lines+markers', name='동경', line=dict(color='black', width=3)))

        # 4. 선택된 함수 요소 강조
        if "sin" in func_type:
            fig_circle.add_trace(go.Scatter(x=[x_val, x_val], y=[0, y_val], mode='lines', name='sin (높이)', line=dict(color='#FF4B4B', width=4)))
        elif "cos" in func_type:
            fig_circle.add_trace(go.Scatter(x=[0, x_val], y=[0, 0], mode='lines', name='cos (밑변)', line=dict(color='#0068C9', width=4)))
        elif "tan" in func_type:
            # tan 접선 (x=1 직선 상의 높이)
            if abs(x_val) > 0.001:
                tan_y = np.tan(angle_rad)
                fig_circle.add_trace(go.Scatter(x=[1, 1], y=[0, tan_y], mode='lines', name='tan (접선 높이)', line=dict(color='#29B6F6', width=4)))
                fig_circle.add_trace(go.Scatter(x=[0, 1], y=[0, tan_y], mode='lines', line=dict(color='gray', dash='dot'), showlegend=False))

        fig_circle.update_layout(
            height=420,
            xaxis=dict(range=[-1.8, 1.8], constrain='domain'),
            yaxis=dict(range=[-1.8, 1.8], scaleanchor="x", scaleratio=1),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_circle, use_container_width=True)

    with col_right:
        st.subheader("삼각함수 파형 그래프")
        x_graph = np.linspace(0, 2*np.pi, 300)

        fig_wave = go.Figure()

        if "sin" in func_type:
            y_graph = np.sin(x_graph)
            curr_y = y_val
            color = '#FF4B4B'
            title_text = "y = sin(θ)"
        elif "cos" in func_type:
            y_graph = np.cos(x_graph)
            curr_y = x_val
            color = '#0068C9'
            title_text = "y = cos(θ)"
        else:
            y_graph = np.tan(x_graph)
            # 탄젠트 점근선 처리 (값이 너무 튀지 않도록 마스킹)
            y_graph[np.abs(y_graph) > 5] = np.nan
            curr_y = np.tan(angle_rad) if abs(angle_deg - 90) > 1 and abs(angle_deg - 270) > 1 else np.nan
            color = '#29B6F6'
            title_text = "y = tan(θ)"

        # 그래프선 및 현재 각도 점 표시
        fig_wave.add_trace(go.Scatter(x=np.degrees(x_graph), y=y_graph, mode='lines', name=title_text, line=dict(color=color, width=3)))
        if not np.isnan(curr_y):
            fig_wave.add_trace(go.Scatter(x=[angle_deg], y=[curr_y], mode='markers', name='현재 위치', marker=dict(color='black', size=12)))

        y_range = [-1.5, 1.5] if "tan" not in func_type else [-4, 4]

        fig_wave.update_layout(
            height=420,
            xaxis=dict(title="각도 (°)", range=[0, 360]),
            yaxis=dict(title="y 값", range=y_range),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_wave, use_container_width=True)

    # 실시간 측정값 표시
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("각도 (θ)", f"{angle_deg}° ({angle_rad:.2f} rad)")
    m2.metric("sin(θ)", f"{y_val:.4f}")
    m3.metric("cos(θ)", f"{x_val:.4f}")
    tan_display = f"{np.tan(angle_rad):.4f}" if abs(x_val) > 0.001 else "정의되지 않음 (∞)"
    m4.metric("tan(θ)", tan_display)

# =========================================================
# 모드 2: 함수 변형 탐구 (y = a * fn(bx + c) + d)
# =========================================================
elif mode == "2. 🎛️ 함수 변형 탐구 (y = a · fn(bx + c) + d)":
    st.header("2. 삼각함수의 계수 변형 탐구")
    st.write("진폭($a$), 주기($b$), 평행이동($c, d$) 변수를 조절하며 **기본 그래프(점선)**와의 차이를 관찰하세요.")

    col_select, col_empty = st.columns([1, 2])
    with col_select:
        fn_choice = st.radio("탐구할 함수 선택", ["sin", "cos", "tan"], horizontal=True)

    col1, col2, col3, col4 = st.columns(4)
    a = col1.slider("진폭 (a)", 0.1, 3.0, 1.0, 0.1)
    b = col2.slider("주기 조절 (b)", 0.5, 3.0, 1.0, 0.1)
    c = col3.slider("x축 평행이동 (c)", -np.pi, np.pi, 0.0, 0.1)
    d = col4.slider("y축 평행이동 (d)", -2.0, 2.0, 0.0, 0.1)

    x = np.linspace(-2*np.pi, 2*np.pi, 500)

    # 함수 계산
    if fn_choice == "sin":
        y_base = np.sin(x)
        y_mod = a * np.sin(b * x + c) + d
        color_code = '#FF4B4B'
    elif fn_choice == "cos":
        y_base = np.cos(x)
        y_mod = a * np.cos(b * x + c) + d
        color_code = '#0068C9'
    else:
        y_base = np.tan(x)
        y_mod = a * np.tan(b * x + c) + d
        # 탄젠트 불연속점 발산 방지
        y_base[np.abs(y_base) > 10] = np.nan
        y_mod[np.abs(y_mod) > 10] = np.nan
        color_code = '#29B6F6'

    fig = go.Figure()
    # 기준 기본 그래프
    fig.add_trace(go.Scatter(x=x, y=y_base, mode='lines', name=f'기본 y = {fn_choice}(x)', line=dict(color='lightgray', dash='dash')))
    # 변형된 그래프
    fig.add_trace(go.Scatter(x=x, y=y_mod, mode='lines', name=f'y = {a:.1f}·{fn_choice}({b:.1f}x + {c:.1f}) + {d:.1f}', line=dict(color=color_code, width=3)))

    y_limit = [-5, 5] if fn_choice != "tan" else [-8, 8]

    fig.update_layout(
        height=450,
        xaxis=dict(title="x (radians)"),
        yaxis=dict(title="y", range=y_limit),
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 핵심 개념 요약 카드
    if fn_choice != "tan":
        period = (2 * np.pi) / abs(b)
        st.success(f"📏 **{fn_choice.upper()} 함수 수식 해석**: 주기 $T = \\frac{{2\\pi}}{{|{b:.1f}|}} = {period:.2f}$ | 최댓값: **{a+d:.2f}** | 최솟값: **{-a+d:.2f}**")
    else:
        period = np.pi / abs(b)
        st.info(f"📏 **TAN 함수 수식 해석**: 주기 $T = \\frac{{\\pi}}{{|{b:.1f}|}} = {period:.2f}$ | 최댓값/최솟값: **없음 (무한히 발산)**")

# =========================================================
# 모드 3: 롤러코스터 물리 트랙 설계
# =========================================================
elif mode == "3. 🎢 롤러코스터 물리 트랙 설계":
    st.header("3. 삼각함수로 만나는 롤러코스터 트랙")
    st.write("각 삼각함수로 트랙 형태를 바꾸고, 카트를 이동시키면서 **순간 경사도(미분값/기울기)**를 관찰해 보세요.")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🎛️ 트랙 설정")
        track_fn = st.selectbox("트랙 파형 선택", ["sin 함수 트랙", "cos 함수 트랙", "tan 함수 트랙"])
        a = st.slider("트랙 높이 (a)", 1.0, 3.0, 2.0, 0.5)
        b = st.slider("굴곡 횟수 (b)", 0.5, 2.0, 1.0, 0.1)
        car_x = st.slider("카트 위치 (x)", -np.pi, np.pi, 0.0, 0.05)

    with c2:
        x = np.linspace(-np.pi, np.pi, 300)

        if "sin" in track_fn:
            y = a * np.sin(b * x)
            car_y = a * np.sin(b * car_x)
            slope = a * b * np.cos(b * car_x) # 순간 기울기
            track_color = '#FF4B4B'
        elif "cos" in track_fn:
            y = a * np.cos(b * x)
            car_y = a * np.cos(b * car_x)
            slope = -a * b * np.sin(b * car_x)
            track_color = '#0068C9'
        else:
            y = a * np.tan(b * x)
            y[np.abs(y) > 10] = np.nan
            car_y = a * np.tan(b * car_x) if abs(np.cos(b * car_x)) > 0.05 else np.nan
            slope = (a * b) / (np.cos(b * car_x)**2) if abs(np.cos(b * car_x)) > 0.05 else np.nan
            track_color = '#29B6F6'

        fig = go.Figure()
        # 트랙
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='트랙', line=dict(color=track_color, width=4)))

        # 카트 및 기울기(접선)
        if car_y is not None and not np.isnan(car_y):
            fig.add_trace(go.Scatter(x=[car_x], y=[car_y], mode='markers', name='카트', marker=dict(color='black', size=14)))
            
            # 접선 방향 그리기
            dx = 0.5
            fig.add_trace(go.Scatter(
                x=[car_x-dx, car_x+dx],
                y=[car_y - slope*dx, car_y + slope*dx],
                mode='lines', name='진행 방향(기울기)', line=dict(color='#FFB703', width=3, dash='dot')
            ))

        fig.update_layout(
            height=420,
            xaxis=dict(range=[-np.pi-0.1, np.pi+0.1]),
            yaxis=dict(range=[-5, 5]),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    # 경사도에 따른 시각적 안내
    if slope is not None and not np.isnan(slope):
        if abs(slope) > 3.0:
            st.error(f"⚠️ 현재 위치의 경사도가 **{slope:.2f}**로 매우 가파릅니다! (급경사 주의)")
        else:
            st.success(f"✅ 현재 위치의 경사도(기울기): **{slope:.2f}** (안전 구간)")
    else:
        st.warning("⚠️ 카트가 트랙이 끊어지는 수직 점근선 위치에 있습니다!")
