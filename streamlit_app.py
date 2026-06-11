import streamlit as st

# 페이지 제목 및 설정
st.set_page_config(page_title="적금 만기금액 계산기", page_icon="💰", layout="centered")

st.title("💰 적금 만기금액 계산기")
st.caption("매월 일정 금액을 납입했을 때의 세후 만기 수령액을 계산합니다.")
st.write("---")

# 레이아웃 분할 (입력창을 깔끔하게 배치)
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("월 납입액 (만원)", min_value=1, value=50, step=5)
    months = st.number_input("납입 기간 (개월)", min_value=1, value=12, step=1)

with col2:
    rate = st.number_input("연 금리 (%)", min_value=0.1, value=4.5, step=0.1, format="%.2f")
    tax_rate = st.selectbox("이자소득세 구분", ["일반과세 (15.4%)", "비과세 (0%)"])

# 세율 설정
tax_percent = 0.154 if "일반과세" in tax_rate else 0.0

# 계산 로직 (버튼 클릭 시 실행)
if st.button("만기 금액 계산하기", type="primary", use_container_width=True):
    # 월리 계산 (연금리 -> 월금리)
    monthly_rate = rate / 100 / 12
    interest = 0
    
    # 적금 이자 계산 (첫 달 넣은 돈은 months개월만큼, 마지막 달 넣은 돈은 1개월만큼 이자가 붙음)
    for i in range(1, months + 1):
        remaining = months - i + 1
        interest += amount * monthly_rate * remaining
        
    # 원금, 세금, 최종 수령액 계산
    principle = amount * months
    tax = interest * tax_percent
    final_amount = principle + interest - tax

    # 결과 화면 출력
    st.write("---")
    st.subheader("📊 계산 결과")
    
    # 메릭스(Metrics) 컴포넌트로 깔끔하게 시각화
    m1, m2 = st.columns(2)
    m1.metric(label="총 납입 원금", value=f"{principle:,.0f} 만원")
    m2.metric(label="세전 이자", value=f"{interest:,.1f} 만원")
    
    m3, m4 = st.columns(2)
    m3.metric(label="이자 소득세", value=f"{tax:,.1f} 만원")
    m4.metric(label="세후 최종 수령액", value=f"{final_amount:,.1f} 만원")
    
    # 강조 효과
    st.success(f"🎉 만기 시 총 **{final_amount:,.0f}만 {(final_amount%1)*10:,.0f}천원**을 받으실 수 있습니다!")
