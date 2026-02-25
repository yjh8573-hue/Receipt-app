import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 설정
st.set_page_config(page_title="영수증 캡처 리포트", layout="wide")

# 우측 상단 추출 버튼 및 UI 스타일링
st.markdown("""
    <style>
    .stDownloadButton { position: fixed; top: 50px; right: 30px; z-index: 999; }
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 영수증 캡처 & 리포트 생성기")
st.write("이미지 파일을 올리거나, 화면 캡처 후 **이 화면에서 Ctrl+V**를 눌러보세요.")

# 2. 이미지 입력 방식 (파일 업로드 + 캡처 이미지 붙여넣기 지원)
# Streamlit의 최신 버전은 붙여넣기를 기본적으로 지원합니다.
img_file = st.file_uploader("영수증 이미지를 업로드하거나 붙여넣으세요", type=['jpg', 'jpeg', 'png'])

if img_file:
    # 이미지 로드
    image = Image.open(img_file).convert("RGB")
    width, height = image.size
    
    # --- [데이터 분석 로직 - 사용자 지정 로직] ---
    supply_val = 120000   # 실제 구현 시 OCR 결과 대입
    delivery_count = 5     # 실제 구현 시 행 개수 인식 결과 대입
    delivery_val = delivery_count * 4000
    total_val = supply_val + delivery_val
    # ------------------------------------------

    # 3. 우측 확장 리포트 생성
    new_width = int(width * 1.5)
    result_img = Image.new("RGB", (new_width, height), (255, 255, 255))
    result_img.paste(image, (0, 0))
    
    draw = ImageDraw.Draw(result_img)
    # 이미지 크기에 맞춰 폰트 크기 조절
    font_size = max(20, int(height / 30))
    try:
        # Streamlit Cloud 환경의 기본 폰트 경로 활용
        font = ImageFont.load_default() 
    except:
        font = ImageFont.load_default()

    margin_left = width + 40
    line_spacing = int(height * 0.1)
    
    draw.text((margin_left, height*0.2), f"• 도시락 공급가액 : {supply_val:,}원", fill=(0, 0, 0), font=font)
    draw.text((margin_left, height*0.2 + line_spacing), f"• 배달 공급가액 : {delivery_count}회 X 4,000원", fill=(0, 0, 0), font=font)
    draw.text((margin_left, height*0.2 + line_spacing*2), f"• 총액 : {total_val:,}원", fill=(220, 20, 60), font=font)

    # 4. 상단 [추출] 버튼 구성
    img_byte_arr = io.BytesIO()
    result_img.save(img_byte_arr, format='JPEG')
    
    st.download_button(
        label="📤 추출 (JPG 저장)",
        data=img_byte_arr.getvalue(),
        file_name="receipt_result.jpg",
        mime="image/jpeg"
    )

    # 5. 화면 표시
    st.image(result_img, caption="분석 완료된 리포트", use_container_width=True)
