import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 기본 설정 및 다크모드 스타일링
st.set_page_config(
    page_title="MathScape - 삼각함수 & 점근선 탐구",
    page_icon="📐",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px;
        color: #94a3b8;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #06b6d4 !important;
        color: #0f172a !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📐 MathScape : 삼각함수 & 점근선 시각화")
st.caption("수학과제탐구 - 인터랙티브 수학 개념 학습 웹 앱")

# 세션 상태 안전 초기화 (기존 버전 오류 수정)
if 'score' not in st.session_state:
    st.session_state['score'] = 0

# 2. 탭 구성
tab1, tab2 = st.tabs(["1. 탄젠트 & 점근선 시각화", "2. 점근선 타격 퀴즈 (Math Breakout)"])

# ---------------------------------------------------------
# TAB 1: 탄젠트 함수 및 점근선 탐구
# ---------------------------------------------------------
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 함수 파라미터 조절")
        b = st.slider("주기 계수 (b)", min_value=0.5, max_value=3.0, value=1.0, step=0.1, key="tan_b")
        c = st.slider("평행이동 (c)", min_value=-3.14, max_value=3.14, value=0.0, step=0.1, key="tan_c")
        
        st.info(f"""
        📌 **수학적 공식 분석**
        - **함수 식:** $y = \\tan({b:.1f}x - ({c:.2f}))$
        - **주기:** $T = \\frac{{\\pi}}{{|b|}} = \\frac{{\\pi}}{{{b:.1f}}}$
        - **점근선 방정식:**  
          $x = \\frac{{n\\pi + \\frac{{\\pi}}{{2}} + {c:.2f}}}{{{b:.1f}}} \\quad (n \\in \\mathbb{{Z}})$
        """)

    with col2:
        # Matplotlib Figure 객체 직접 생성 (Streamlit 권장 방식)
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#020617')
        
        x = np.linspace(-3 * np.pi, 3 * np.pi, 2000)
        y = np.tan(b * x - c)
        
        # 불연속점(점근선 연결) 제거
        y[np.abs(y) > 10] = np.nan
        
        # 탄젠트 곡선 및 축
        ax.plot(x, y, color='#06b6d4', linewidth=2.5, label=f'y = tan({b}x - {c})')
        ax.axhline(0, color='#334155', linewidth=1)
        ax.axvline(0, color='#334155', linewidth=1)
        
        # 점근선(Asymptote) 그리기
        for n in range(-10, 11):
            asymptote_x = (n * np.pi + np.pi / 2 + c) / b
            if -3 * np.pi <= asymptote_x <= 3 * np.pi:
                ax.axvline(x=asymptote_x, color='#ef4444', linestyle='--', linewidth=1.5, alpha=0.8)
        
        ax.set_xlim([-3 * np.pi, 3 * np.pi])
        ax.set_ylim([-5, 5])
        ax.tick_params(colors='#94a3b8')
        for spine in ax.spines.values():
            spine.set_color('#334155')
            
        ax.set_title("Tangent Function & Asymptotes", color='#f8fafc', fontsize=12, pad=12)
        st.pyplot(fig)
        plt.close(fig)  # 메모리 누수 방지

# ---------------------------------------------------------
# TAB 2: 점근선 타격 퀴즈 모드
# ---------------------------------------------------------
with tab2:
    st.subheader("🎯 점근선 타격 미션")
    st.write("슬라이더를 조작하여 탄젠트 그래프의 점근선을 빨간색 목표 위치($x = -\\frac{\\pi}{2}, \\frac{\\pi}{2}$)에 일치시키세요!")

    quiz_b = st.slider("퀴즈 - 그래프 주기 계수 조절 (b)", min_value=0.5, max_value=3.0, value=1.0, step=0.5, key="quiz_b_slider")
    
    target_targets = [-np.pi / 2, np.pi / 2]
    player_asymptotes = [(n * np.pi + np.pi / 2) / quiz_b for n in range(-5, 6)]
    
    # 성공 여부 체크
    hit_count = 0
    for target in target_targets:
        if any(abs(target - asymp) < 0.05 for asymp in player_asymptotes):
            hit_count += 1

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    fig2.patch.set_facecolor('#0f172a')
    ax2.set_facecolor('#020617')
    
    # 타겟 블록 표시
    for target in target_targets:
        is_hit = any(abs(target - asymp) < 0.05 for asymp in player_asymptotes)
        color = '#10b981' if is_hit else '#ef4444'
        label_text = "HIT!" if is_hit else "TARGET"
        
        ax2.axvline(x=target, color=color, linewidth=4, alpha=0.9)
        ax2.text(target, 3.5, f" {label_text}\n(x={target:.2f})", color=color, fontweight='bold', ha='center')

    # 플레이어의 점근선
    for asymp in player_asymptotes:
        if -2 * np.pi <= asymp <= 2 * np.pi:
            ax2.axvline(x=asymp, color='#06b6d4', linestyle=':', linewidth=1.5)

    ax2.axhline(0, color='#334155', linewidth=1)
    ax2.set_xlim([-2 * np.pi, 2 * np.pi])
    ax2.set_ylim([-5, 5])
    ax2.tick_params(colors='#94a3b8')
    for spine in ax2.spines.values():
        spine.set_color('#334155')

    st.pyplot(fig2)
    plt.close(fig2)

    # 결과 메시지
    if hit_count == len(target_targets):
        st.success("🎉 성공! 모든 목표 점근선 위치를 완벽하게 타격했습니다!")
    else:
        st.warning(f"현재 {hit_count}/{len(target_targets)}개 목표 적중. 주기 계수 b를 조절해보세요.")
