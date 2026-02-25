import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="최종 보안 해결 리포트", layout="wide")

st.title("🛡️ 보안 환경 최적화 리포트 생성기")

# 1. 카메라 입력 기능 활용 (보안망에서 가장 잘 작동)
# 'Take a Photo' 버튼을 누르면 브라우저 팝업이 뜹니다. 
# 거기서 '화면 공유' 또는 '웹캠'을 선택할 수 있는데, 이를 이용해 영수증을 찍습니다.
img_file = st.camera_input("영수증을 화면에 띄우고 아래 'Take Photo'를 누르세요")

if img_file:
    try:
        image = Image.open(img_file).convert("RGB")
        width, height = image.size
        
        # [임시 계산 로직]
        supply_val = 150000 
        delivery_count = 5 
        delivery_val = delivery_count * 4000
        total_val = supply_val + delivery_val

        # 리포트 생성
        new_width = int(width * 1.5)
        result_img = Image.new("RGB", (new_width, height), (255, 255, 255))
        result_img.paste(image, (0, 0))
        draw = ImageDraw.Draw(result_img)
        font = ImageFont.load_default()

        margin_left = width + 30
        draw.text((margin_left, height*0.2), f"도시락 공급가액 : {supply_val:,}원", fill=(0,0,0), font=font)
        draw.text((margin_left, height*0.3), f"배달 공급가액 : {delivery_count}회 X 4,000원", fill=(0,0,0), font=font)
        draw.text((margin_left, height*0.4), f"총액 : {total_val:,}원", fill=(255,0,0), font=font)

        st.image(result_img, use_container_width=True)
        
        buf = io.BytesIO()
        result_img.save(buf, format="JPEG")
        st.download_button("📤 추출 (JPG 저장)", buf.getvalue(), "report.jpg", "image/jpeg")
        
    except Exception as e:
        st.error("이미지를 처리할 수 없습니다.")
