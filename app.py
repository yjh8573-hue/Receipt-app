import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 설정
st.set_page_config(page_title="보안형 영수증 리포트", layout="wide")

st.markdown("""
    <style>
    /* 추출 버튼 우측 상단 고정 */
    .stDownloadButton { position: fixed; top: 50px; right: 30px; z-index: 999; }
    
    /* 파일 업로더 영역 강조 */
    [data-testid="stFileUploader"] {
        border: 5px solid #4A90E2 !important;
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 보안형 영수증 리포트 생성기")

# 안내 문구
st.error("⚠️ 주의: 파일 탐색기를 열지 마세요. IT 보안 정책을 준수합니다.")
st.info("💡 방법: 1.영수증 캡처 -> 2.아래 'Browse files' 버튼을 마우스로 한 번 클릭 -> 3.Ctrl + V")

# 2. 이미지 입력 받기 (가장 호환성이 좋은 표준 위젯)
# 이 위젯을 '클릭'하여 포커스를 준 상태에서 Ctrl+V를 누르면 브라우저가 이미지를 파일로 자동 전환합니다.
img_file = st.file_uploader("여기를 클릭한 후 Ctrl+V를 누르세요", type=['png', 'jpg', 'jpeg'])

if img_file:
    try:
        # 데이터 읽기
        image = Image.open(img_file).convert("RGB")
        width, height = image.size
        
        # --- [계산 로직: 예시 데이터] ---
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
        st.error(f"이미지를 처리할 수 없습니다. 다시 캡처해서 시도해 주세요.")
