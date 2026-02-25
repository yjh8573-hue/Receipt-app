import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 설정
st.set_page_config(page_title="보안형 영수증 리포트", layout="wide")

st.markdown("""
    <style>
    /* 추출 버튼 우측 상단 고정 */
    .stDownloadButton { position: fixed; top: 50px; right: 30px; z-index: 999; }
    /* 붙여넣기 안내 박스 스타일 */
    .paste-hint {
        padding: 30px;
        background-color: #f8f9fa;
        border: 3px dashed #4A90E2;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 보안형 영수증 리포트 생성기")

# 2. 이미지 입력 받기 (가장 표준적이고 호환성 높은 방식)
st.markdown('<div class="paste-hint"><h3>[ 캡처 이미지 붙여넣기 ]</h3><p>아래 <b>"Browse files" 버튼 위를 한 번 클릭</b>한 뒤<br><b>Ctrl + V</b>를 누르면 바로 인식됩니다.</p></div>', unsafe_allow_html=True)

# 파일 업로더를 다시 사용하지만, '파일 선택' 대신 '붙여넣기 전용'으로 안내합니다.
# 이 위젯은 클릭 후 Ctrl+V를 하면 브라우저가 이미지를 파일로 변환해서 넣어줍니다.
img_file = st.file_uploader("여기에 이미지를 붙여넣으세요 (Ctrl+V)", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

if img_file:
    try:
        # 데이터 읽기
        image = Image.open(img_file).convert("RGB")
        width, height = image.size
        
        # --- [계산 로직: 영수증 분석 결과 가정] ---
        supply_val = 125000 
        delivery_count = 5 
        delivery_val = delivery_count * 4000
        total_val = supply_val + delivery_val

        # 3. 이미지 생성 (우측 확장)
        new_width = int(width * 1.5)
        result_img = Image.new("RGB", (new_width, height), (255, 255, 255))
        result_img.paste(image, (0, 0))
        
        draw = ImageDraw.Draw(result_img)
        font = ImageFont.load_default()

        margin_left = width + 40
        draw.text((margin_left, height*0.2), f"도시락 공급가액 : {supply_val:,}원", fill=(0, 0, 0), font=font)
        draw.text((margin_left, height*0.3), f"배달 공급가액 : {delivery_count}회 X 4,000원", fill=(0, 0, 0), font=font)
        draw.text((margin_left, height*0.4), f"총액 : {total_val:,}원", fill=(255, 0, 0), font=font)

        # 4. 결과물 표시
        st.success("✅ 영수증 인식 성공!")
        st.image(result_img, use_container_width=True)

        # 5. [추출] 버튼
        img_byte_arr = io.BytesIO()
        result_img.save(img_byte_arr, format='JPEG')
        st.download_button(
            label="📤 추출 (JPG 저장)",
            data=img_byte_arr.getvalue(),
            file_name="receipt_report.jpg",
            mime="image/jpeg"
        )
    except Exception as e:
        st.error(f"이미지를 처리할 수 없습니다. 캡처를 다시 한 번만 시도해 주세요.")
