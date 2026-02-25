import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 페이지 설정
st.set_page_config(page_title="영수증 리포트 생성기", layout="wide")

# CSS로 우측 상단 추출 버튼 스타일링
st.markdown("""
    <style>
    .stDownloadButton {
        position: fixed;
        top: 50px;
        right: 30px;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 영수증 최종 레포트 생성기")
st.info("영수증을 업로드하면 자동으로 계산된 텍스트가 우측에 추가됩니다.")

uploaded_file = st.file_uploader("영수증 이미지를 선택하세요", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    # 1. 이미지 로드
    image = Image.open(uploaded_file).convert("RGB")
    width, height = image.size
    
    # 2. 로직 처리 (예시 데이터 - 실제 운영 시 OCR 라이브러리 연동 가능)
    # 여기서는 사용자 요청에 따른 계산 로직을 시뮬레이션합니다.
    supply_val = 120000  # 실제로는 영수증 인식 값 입력
    delivery_count = 5    # 실제로는 행 개수 카운트 값 입력
    delivery_val = delivery_count * 4000
    total_val = supply_val + delivery_val
    
    # 3. 우측 텍스트 영역 확장 (원본 너비의 40% 추가)
    new_width = int(width * 1.4)
    result_img = Image.new("RGB", (new_width, height), (255, 255, 255))
    result_img.paste(image, (0, 0))
    
    # 4. 텍스트 삽입
    draw = ImageDraw.Draw(result_img)
    # 폰트 사이즈는 이미지 높이에 비례하게 설정
    font_size = int(height / 25) 
    try:
        font = ImageFont.truetype("NanumGothic.ttf", font_size)
    except:
        font = ImageFont.load_default()

    margin_left = width + 30
    draw.text((margin_left, height*0.1), f"도시락 공급가액 : {supply_val:,}원", fill=(0, 0, 0), font=font)
    draw.text((margin_left, height*0.2), f"배달 공급가액 : {delivery_count}회 X 4,000원", fill=(0, 0, 0), font=font)
    draw.text((margin_left, height*0.3), f"총액 : {total_val:,}원", fill=(255, 0, 0), font=font)

    # 5. [추출] 버튼 (우측 상단 고정)
    img_byte_arr = io.BytesIO()
    result_img.save(img_byte_arr, format='JPEG')
    btn = st.download_button(
        label="📥 추출 (JPG 저장)",
        data=img_byte_arr.getvalue(),
        file_name="final_report.jpg",
        mime="image/jpeg"
    )

    # 6. 화면 표시
    st.image(result_img, use_column_width=True)
