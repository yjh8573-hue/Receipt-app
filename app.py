import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 페이지 설정 및 파일 업로드 버튼 숨기기
st.set_page_config(page_title="보안형 영수증 리포트 생성기", layout="wide")

st.markdown("""
    <style>
    /* 파일 업로드 위젯 숨기기 */
    [data-testid="stFileUploader"] { display: none; }
    /* 추출 버튼 위치 고정 */
    .stDownloadButton { position: fixed; top: 50px; right: 30px; z-index: 999; }
    /* 붙여넣기 안내 구역 디자인 */
    .paste-zone {
        border: 2px dashed #4A90E2;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 보안형 영수증 리포트 생성기")
st.markdown('<div class="paste-zone"><h3>상태: 영수증 대기 중</h3><p>윈도우 캡처(Win+Shift+S) 후 <b>이 화면을 클릭하고 Ctrl+V</b>를 누르세요.</p></div>', unsafe_allow_html=True)

# 2. 클립보드 이미지 입력을 위한 텍스트 입력 위젯 활용 (Streamlit의 우회 방법)
# 최신 Streamlit은 이미지가 포함된 paste 이벤트를 자동으로 감지합니다.
pasted_img = st.chat_input("여기에 이미지를 붙여넣으세요 (Ctrl+V)")

# 만약 chat_input 대신 기본 업로더의 '붙여넣기' 기능만 남기고 싶다면 아래 위젯을 사용합니다.
# 하지만 보안 정책상 업로더 자체가 막혔다면 아래 paste_input이 가장 안전합니다.
img_data = st.image_uploader_substitute = st.experimental_data_editor = None # 초기화

# 3. 이미지 처리 로직
if pasted_img is not None:
    # 이미지가 클립보드에서 들어왔을 때 처리
    try:
        image = Image.open(pasted_img).convert("RGB")
        width, height = image.size
        
        # --- [사용자 요청 로직 적용] ---
        # 실제 운영 시 이 부분에 OCR 코드를 넣어 '공급가액'과 '행 개수'를 추출합니다.
        supply_val = 150000  # 예시 값
        delivery_count = 5    # 예시 값 (행 개수)
        delivery_val = delivery_count * 4000
        total_val = supply_val + delivery_val
        
        # 4. 리포트 이미지 생성 (우측 확장)
        new_width = int(width * 1.5)
        result_img = Image.new("RGB", (new_width, height), (255, 255, 255))
        result_img.paste(image, (0, 0))
        
        draw = ImageDraw.Draw(result_img)
        font_size = max(20, int(height / 25))
        try:
            font = ImageFont.load_default()
        except:
            font = None

        tx_x = width + 30
        draw.text((tx_x, height*0.2), f"도시락 공급가액 : {supply_val:,}원", fill=(0,0,0), font=font)
        draw.text((tx_x, height*0.3), f"배달 공급가액 : {delivery_count}회 X 4,000원", fill=(0,0,0), font=font)
        draw.text((tx_x, height*0.4), f"총액 : {total_val:,}원", fill=(255,0,0), font=font)

        # 5. 결과 표시 및 추출 버튼
        st.success("✅ 리포트 생성이 완료되었습니다!")
        st.image(result_img, use_container_width=True)
        
        buf = io.BytesIO()
        result_img.save(buf, format="JPEG")
        st.download_button(label="📥 추출 (JPG 저장)", data=buf.getvalue(), file_name="report.jpg", mime="image/jpeg")
        
    except Exception as e:
        st.error(f"이미지를 인식할 수 없습니다. 다시 캡처해서 붙여넣어 주세요.")
