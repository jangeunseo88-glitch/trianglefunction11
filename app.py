import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="인터랙티브 삼각함수 교실",
    page_icon="📐",
    layout="wide"
)

# Custom CSS로 디자인 깔끔하게 다듬기
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.title("📐 한 눈에 이해하는 인터랙티브 삼각함수")
st.caption("20년차 수학 교사와 앱 개발자가 만든 '보고, 듣고, 조작하는' 수학 탐구실")

# 사이드바 모드 선택
st.sidebar.header("🕹️ 탐구 모드 선택")
mode = st.sidebar.radio(
    "원하는 학습 모드를 선택하세요",
    [
        "1. 단위원과 그래프 & 🔊 소리 듣기",
        "2. 🎛️ $y = a \cdot \sin(bx + c) + d$ 변수 탐구",
        "3. 🎢 롤러코스터 물리 트랙 설계",
        "4. 🎯 삼각함수 스나이퍼 게임"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **팁**: 슬라이더를 조작하면서 그래프의 변화를 직관적으로 관찰해 보세요!")

# =========================================================
# 모드 1: 단위원과 그래프 & 소리 듣기
# =========================================================
if mode == "1. 단위원과 그래프 & 🔊 소리 듣기":
    st.header("1. 단위원의 움직임과 삼각함수 파형")
    st.write("단위원 상의 점이 회전할 때, **높이($y$)가 $\sin$**, **밑변($x$)이 $\cos$**가 되는 과정을 확인하세요.")
    
    col_ctrl, col_sound = st.columns([2, 1])
    with col_ctrl:
        angle_deg = st.slider("각도 $\theta$ (도)", 0, 360, 45, step=5)
        angle_rad = np.radians(angle_deg)
    
    with col_sound:
        # 주파수 변환 (각도 45도~360도를 261Hz(도)~523Hz(높은 도) 소리로 매핑)
        freq = int(261.63 + (angle_deg / 360) * (523.25 - 261.63))
        sound_html = f"""
        <script>
        function playTone() {{
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime({freq}, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.8);
        }}
        </script>
        <button onclick="playTone()" style="
            background-color: #4FFF8A; color: #111; border: none; font-weight: bold;
            padding: 10px 20px; font-size: 15px; border-radius: 8px; cursor: pointer; width: 100%; margin-top: 15px;">
            🔊 현재 높이 소리 듣기 ({freq}Hz)
        </button>
        """
        components.html(sound_html, height=70)

    # 2열 시각화
    col1, col2 = st.columns(2)
    x_val, y_val = np.cos(angle_rad), np.sin(angle_rad)

    with col1:
        st.subheader("단위원 (Unit Circle)")
        fig_circle = go.Figure()
        
        # 단위원 테두리
        t_circle = np.linspace(0, 2*np.pi, 200)
        fig_circle.add_trace(go.Scatter(x=np.cos(t_circle), y=np.sin(t_circle), mode='lines', name='단위원', line=dict(color='gray', dash='dash')))
        
        # 축 및 동경
        fig_circle.add_trace(go.Scatter(x=[-1.2, 1.2], y=[0, 0], mode='lines', line=dict(color='lightgray'), showlegend=False))
        fig_circle.add_trace(go.Scatter(x=[0, 0], y=[-1.2, 1.2], mode='lines', line=dict(color='lightgray'), showlegend=False))
        fig_circle.add_trace(go.Scatter(x=[0, x_val], y=[0, y_val], mode='lines+markers', name='동경', line=dict(color='black', width=3)))
        
        # sin(높이-빨강), cos(밑변-파랑)
        fig_circle.add_trace(go.Scatter(x=[x_val, x_val], y=[0, y_val], mode='lines', name='sin (Y 높이)', line=dict(color='#FF4B4B', width=4)))
        fig_circle.add_trace(go.Scatter(x=[0, x_val], y=[0, 0], mode='lines', name='cos (X 길이)', line=dict(color='#0068C9', width=4)))

        fig_circle.update_layout(
            height=400,
            xaxis=dict(range=[-1.3, 1.3], constrain='domain'),
            yaxis=dict(range=[-1.3, 1.3], scaleanchor="x", scaleratio=1),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_circle, use_container_width=True)

    with col2:
        st.subheader("$y = \sin(\\theta)$ 파형")
        x_graph = np.linspace(0, 2*np.pi, 200)
        y_graph = np.sin(x_graph)

        fig_wave = go.Figure()
        fig_wave.add_trace(go.Scatter(x=np.degrees(x_graph), y=y_graph, mode='lines', name='sin wave', line=dict(color='lightgray', width=2)))
        fig_wave.add_trace(go.Scatter(x=[angle_deg], y=[y_val], mode='markers', name='현재 위치', marker=dict(color='#FF4B4B', size=14)))

        fig_wave.update_layout(
            height=400,
            xaxis=dict(title="각도 (°)", range=[0, 360]),
            yaxis=dict(title="y 값", range=[-1.3, 1.3]),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_wave, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("각도 (θ)", f"{angle_deg}° ({angle_rad:.2f} rad)")
    m2.metric("sin(θ) [높이]", f"{y_val:.4f}")
    m3.metric("cos(θ) [밑변]", f"{x_val:.4f}")

# =========================================================
# 모드 2: y = a*sin(bx + c) + d 변수 탐구
# =========================================================
elif mode == "2. 🎛️ $y = a \cdot \sin(bx + c) + d$ 변수 탐구":
    st.header("2. 삼각함수의 변형 파라미터 탐구")
    st.write("각 변수가 그래프의 **진폭, 주기, 평행이동**에 어떤 영향을 주는지 직접 확인해보세요.")

    col1, col2, col3, col4 = st.columns(4)
    a = col1.slider("진폭 (a)", 0.1, 3.0, 1.0, 0.1)
    b = col2.slider("주기 조절 (b)", 0.5, 3.0, 1.0, 0.1)
    c = col3.slider("x축 이동 (c)", -np.pi, np.pi, 0.0, 0.1)
    d = col4.slider("y축 이동 (d)", -2.0, 2.0, 0.0, 0.1)

    x = np.linspace(-2*np.pi, 2*np.pi, 500)
    y_base = np.sin(x)
    y_mod = a * np.sin(b * x + c) + d

    fig = go.Figure()
    # 기준 그래프 (원래 sin(x))
    fig.add_trace(go.Scatter(x=x, y=y_base, mode='lines', name='기본 y = sin(x)', line=dict(color='lightgray', dash='dash')))
    # 변형된 그래프
    fig.add_trace(go.Scatter(x=x, y=y_mod, mode='lines', name='변형된 그래프', line=dict(color='#83C5BE', width=3)))

    fig.update_layout(
        height=450,
        xaxis=dict(title="x"),
        yaxis=dict(title="y", range=[-5, 5]),
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    period = (2 * np.pi) / abs(b)
    st.success(f"📏 **현재 공식의 특징**: 주기 $T = \\frac{{2\\pi}}{{|{b:.1f}|}} = {period:.2f}$ | 최댓값: **{a+d:.2f}** | 최솟값: **{-a+d:.2f}**")

# =========================================================
# 모드 3: 롤러코스터 물리 트랙 설계
# =========================================================
elif mode == "3. 🎢 롤러코스터 물리 트랙 설계":
    st.header("3. 삼각함수로 만드는 롤러코스터 트랙")
    st.write("트랙의 높낮이와 굴곡을 삼각함수로 설계하고, 카트를 이동시키며 **경사도(접선 기울기)**를 관찰하세요.")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🎛️ 트랙 및 카트 조절")
        a = st.slider("트랙 높이 (a)", 1.0, 4.0, 2.5, 0.5)
        b = st.slider("굴곡 횟수 (b)", 0.5, 2.0, 1.0, 0.1)
        car_x = st.slider("카트 위치 (x)", -np.pi, np.pi, 0.0, 0.1)

    with c2:
        x = np.linspace(-np.pi, np.pi, 300)
        y = a * np.sin(b * x)

        # 카트 위치 계산
        car_y = a * np.sin(b * car_x)
        slope = a * b * np.cos(b * car_x) # 순간 기울기 (미분)

        fig = go.Figure()
        # 트랙
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='롤러코스터 트랙', line=dict(color='#2B2D42', width=5)))
        # 카트
        fig.add_trace(go.Scatter(x=[car_x], y=[car_y], mode='markers', name='카트', marker=dict(color='#D80032', size=16)))
        # 접선 (기울기)
        dx = 0.6
        fig.add_trace(go.Scatter(
            x=[car_x-dx, car_x+dx], 
            y=[car_y - slope*dx, car_y + slope*dx],
            mode='lines', name='진행 방향 (기울기)', line=dict(color='#FFB703', width=3, dash='dot')
        ))

        fig.update_layout(
            height=400,
            xaxis=dict(range=[-np.pi-0.2, np.pi+0.2]),
            yaxis=dict(range=[-5, 5]),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    if abs(slope) > 2.5:
        st.error(f"⚠️ 현재 경사도가 **{slope:.2f}**로 매우 가파릅니다! 카트가 추락할 위험이 있습니다!")
    else:
        st.info(f"✅ 현재 경사도(기울기): **{slope:.2f}** (안전한 구간입니다)")

# =========================================================
# 모드 4: 삼각함수 스나이퍼 게임
# =========================================================
elif mode == "4. 🎯 삼각함수 스나이퍼 게임":
    st.header("4. 삼각함수 스나이퍼 게임")
    st.write("주어진 **3개의 타겟 🎯**을 모두 정확히 통과하도록 $a$와 $b$ 값을 조절해 레이저를 쏘세요!")

    # Target points
    targets_x = np.array([np.pi/4, np.pi/2, 3*np.pi/2])
    targets_y = np.array([1.414, 2.0, -2.0])

    c_input, c_plot = st.columns([1, 2])
    
    with c_input:
        st.subheader("🎯 레이저 조준장치")
        user_a = st.number_input("진폭 (a) 조절", value=1.0, step=0.5, format="%.1f")
        user_b = st.number_input("주기 (b) 조절", value=1.0, step=0.5, format="%.1f")

        # 명중 여부 계산
        user_y_at_targets = user_a * np.sin(user_b * targets_x)
        errors = np.abs(user_y_at_targets - targets_y)

        if np.all(errors < 0.25):
            st.balloons()
            st.success("🎉 MISSION COMPLETE! 모든 타겟을 정확히 적중시켰습니다!")
        else:
            st.warning("🎯 타겟의 위치를 맞추기 위해 $a$와 $b$를 계속 조절하세요.")

    with c_plot:
        x_line = np.linspace(0, 2*np.pi, 300)
        y_line = user_a * np.sin(user_b * x_line)

        fig_game = go.Figure()
        # 발사되는 레이저
        fig_game.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='발사 레이저', line=dict(color='#FF4B4B', width=3)))
        # 타겟점들
        fig_game.add_trace(go.Scatter(
            x=targets_x, y=targets_y, mode='markers', name='타겟 🎯',
            marker=dict(color='#00CC66', size=18, symbol='target')
        ))

        fig_game.update_layout(
            height=400,
            xaxis=dict(title="x", range=[0, 2*np.pi]),
            yaxis=dict(title="y", range=[-3.5, 3.5]),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_game, use_container_width=True)
