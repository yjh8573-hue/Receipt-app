import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="보안형 영수증 리포트", layout="wide")

# UI 디자인 개선
st.markdown("""
    <style>
    [data-testid="stFileUploader"] { display: none; }
    .stDownloadButton { position: fixed; top: 50px; right: 30px; z-index: 999; }
    .stTextInput input {
        height: 100px;
        font-size: 20px !important;
        text-align: center;
        border: 2px solid #4A90E2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 보안형 영수증 리포트 생성기")

# 중앙에 강조된 입력창 배치
st.info("아래 입력창을 클릭한 후 Ctrl+V를 누르세요!")
pasted_data = st.text_input("👇 여기에 마우스 클릭 후 붙여넣기(Ctrl+V)", placeholder="이미지를 붙여넣으면 아래에 리포트가 생성됩니다.")

# Streamlit에서 클립보드 이미지를 처리하는 로직
# (참고: 웹 브라우저 제약으로 인해 텍스트 입력창에 이미지를 넣으면 파일 형태 데이터로 자동 변환됩니다)
if pasted_data:
    # 텍스트 입력창에 이미지가 들어오면 보통 임시 경로가 생성됩니다.
    # 만약 위 방법이 회사 보안망에서 차단된다면, 가장 확실한 방법은 
    # 하단의 'chat_input'을 사용하는 것입니다.
    pass

# 가장 권장하는 보안 환경용 '붙여넣기' 위젯
pasted_img = st.chat_input("여기에 영수증 이미지를 붙여넣으세요")

if pasted_img:
    try:
        # 이미지를 열고 분석 시작
        image = Image.open(pasted_img).convert("RGB")
        width, height = image.size
        
        # [임시 계산 로직] - 나중에 실제 OCR 연동 시 수정
        supply = 150000
        count = 5
        delivery = count * 4000
        total = supply + delivery
        
        # 이미지 우측 확장 및 텍스트 기입
        new_width = int(width * 1.5)
        res = Image.new("RGB", (new_width, height), (255, 255, 255))
        res.paste(image, (0,0))
        draw = ImageDraw.Draw(res)
        font = ImageFont.load_default()
        
        draw.text((width + 20, height*0.2), f"도시락 공급가액 : {supply:,}원", fill=(0,0,0), font=font)
        draw.text((width + 20, height*0.3), f"배달 공급가액 : {count}회 X 4,000원", fill=(0,0,0), font=font)
        draw.text((width + 20, height*0.4), f"총액 : {total:,}원", fill=(255,0,0), font=font)
        
        st.image(res, caption="리포트 생성 완료", use_container_width=True)
        
        # 추출 버튼
        buf = io.BytesIO()
        res.save(buf, format="JPEG")
        st.download_button("📤 추출 (JPG 저장)", buf.getvalue(), "report.jpg", "image/jpeg")
        
    except:
        st.error("이미지 형식이 아닙니다. 캡처 후 다시 붙여넣어 주세요.")
