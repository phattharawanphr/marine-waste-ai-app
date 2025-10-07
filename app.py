import streamlit as st
from inference_sdk import InferenceHTTPClient
from PIL import Image

# ตั้งค่า client ของ Roboflow
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="TCwrOT5oJu5pTNpnNKSV"
)

st.set_page_config(page_title="🌊 Marine Waste AI", page_icon="🌊")
st.title("🌊 Marine Waste AI")
st.markdown("แอปนี้ช่วยจำแนกประเภทของขยะทะเล โดยใช้โมเดล AI ที่พัฒนาใน Roboflow")

uploaded = st.file_uploader("📤 อัปโหลดภาพขยะ", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    image.save("temp.jpg")
    st.image(image, caption="ภาพที่อัปโหลด", use_column_width=True)

    with st.spinner("🔍 กำลังวิเคราะห์..."):
        result = CLIENT.infer("temp.jpg", model_id="marine-waste-ai-wb2eb/3")

    pred_class = result["predictions"][0]["class"]
    confidence = result["predictions"][0]["confidence"] * 100

    st.success(f"✅ ผลลัพธ์: **{pred_class}** ({confidence:.2f}%)")
    st.balloons()
