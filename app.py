import streamlit as st
from inference_sdk import InferenceHTTPClient
from PIL import Image

#ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="🌊 Marine Waste AI",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

#กำหนดสีพื้นหลัง
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #e0f7fa, #ffffff);
}
[data-testid="stSidebar"] {
    background-color: #b3e5fc;
}
h1, h2, h3, h4, h5 {
    color: #01579b;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

#ตั้งค่า client ของ Roboflow
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="TCwrOT5oJu5pTNpnNKSV"
)

# ---------- Sidebar: About ----------
st.sidebar.title("🌐 Marine Waste AI")
st.sidebar.markdown("---")
st.sidebar.header("📘 About the Developer")
st.sidebar.markdown("""
**ชื่อ:** นางสาวภัทราวรรณ พรหมเรืองฤทธิ์  
**สถานะ:** นักศึกษาคณะเทคนิคการแพทย์    
**รหัสนักศึกษา:** 681110071 🎓  

---

โครงการ **Marine Waste AI** พัฒนาเพื่อช่วยจำแนกประเภทของขยะทะเล  
เช่น พลาสติก โลหะ แก้ว และเศษอาหารอื่น ๆ  
โดยใช้โมเดล AI ที่ฝึกจาก Roboflow  

🌊 **เป้าหมายของโครงการ:**  
- สร้างความตระหนักรู้เกี่ยวกับปัญหามลพิษทางทะเล  
- ใช้เทคโนโลยี AI เพื่อสนับสนุนการอนุรักษ์สิ่งแวดล้อม  

---

💻 Powered by [Streamlit](https://streamlit.io) & [Roboflow](https://roboflow.com)
""")

# ---------- ส่วนหลักของหน้าเว็บ ----------
st.title("🌊 Marine Waste AI")
st.write("อัปโหลดภาพเพื่อให้ AI จำแนกประเภทของขยะทะเล")

uploaded = st.file_uploader("📤 เลือกรูปภาพ", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    image.save("temp.jpg")
    st.image(image, caption="ภาพที่อัปโหลด", use_container_width=True)

    with st.spinner("🔍 กำลังวิเคราะห์..."):
        result = CLIENT.infer("temp.jpg", model_id="marine-waste-ai-wb2eb/3")

    pred_class = result["predictions"][0]["class"]
    confidence = result["predictions"][0]["confidence"] * 100

    st.success(f"✅ ผลลัพธ์: **{pred_class}** ({confidence:.2f}%)")
    st.balloons()
