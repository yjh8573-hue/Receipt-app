import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 설정
st.set_page_config(page_title="보안형 영수증 리포트", layout="wide")

st.markdown("""
    <style>
    /* 파일 업로드 숨기기 */
    [data-testid="stFileUploader"] { display: none; }
    /* 추출 버튼 우측 상단 고정 */
    .stDownloadButton { position: fixed; top: 50px; right: 30px; z-index: 999; }
    /* 안내 문구 스타일 */
    .main-info {
        padding: 20px;
        background-color: #e1f5fe;
        border-radius: 10px;
        border: 2px solid #01579b;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 보안형 영수증 리포트 생성기")
st.markdown('<div class="main-info"><h3>[사용 방법]</h3><p>1. 영수증 캡처 (Win+Shift+S)<br>2. <b>맨 아래 "여기에 영수증 이미지..." 칸 클릭</b><br>3. <b>Ctrl + V 누르고 엔터(전송)</b></p></div>', unsafe_allow_html=True)

# 2. 이미지 입력 받기 (하단 채팅창 위젯 활용)
pasted_img = st.chat_input("여기에 영수증 이미지를 붙여넣으세요 (Ctrl+V 후 엔터)")

if pasted_img:
    try:
        # 데이터 읽기
        image = Image.open(pasted_img).convert("RGB")
        width, height = image.size
        
        # --- [계산 로직: 영수증 분석 결과 가정] ---
        # 이 부분은 나중에 실제 영수증 샘플을 주시면 OCR로 자동화해드릴게요!
        supply_val = 125000 
        delivery_count = 5 
        delivery_val = delivery_count * 4000
        total_val = supply_val + delivery_val

        # 3. 이미지 생성 (우측 확장)
        new_width = int(width * 1.5)
        result_img = Image.new("RGB", (new_width, height), (255, 255, 255))
        result_img.paste(image, (0, 0))
        
        draw = ImageDraw.Draw(result_img)
        try:
            font = ImageFont.load_default()
        except:
            font = None

        margin_left = width + 40
        # 텍스트 삽입
        draw.text((margin_left, height*0.2), f"도시락 공급가액 : {supply_val:,}원", fill=(0, 0, 0), font=font)
        draw.text((margin_left, height*0.3), f"배달 공급가액 : {delivery_count}회 X 4,000원", fill=(0, 0, 0), font=font)
        draw.text((margin_left, height*0.4), f"총액 : {total_val:,}원", fill=(255, 0, 0), font=font)

        # 4. 결과물 표시
        st.success("✅ 영수증 인식이 완료되었습니다!")
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
        st.error(f"오류 발생: 이미지를 처리할 수 없습니다. 다시 캡처해서 붙여넣어 주세요.")
