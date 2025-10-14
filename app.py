import streamlit as st
from PIL import Image
import io, base64, requests, time

# ตั้งค่าหน้าเว็บ 
st.set_page_config(
    page_title="🌊 Marine Waste AI",
    page_icon="🪸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# พื้นหลังและเอฟเฟกต์ฟองอากาศ
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(to bottom right, #dbeeff, #f7fbfd);
  animation: fadeIn 2s ease-in;
  overflow: hidden;
}
[data-testid="stSidebar"] {
  background: linear-gradient(to bottom, #cfe0f1, #e3f2fd);
  color: #01579b;
}
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}
h1, h2, h3, h4, h5 {
  color: #01579b;
  font-weight: 700;
  text-shadow: 1px 1px 2px #b0bec5;
}
.result-box {
  background-color: #e8f4fd;
  padding: 20px;
  border-radius: 15px;
  border: 2px solid #64b5f6;
  box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
  animation: fadeIn 1.5s ease-in;
}
footer {
  text-align: center;
  font-size: 0.9em;
  color: #0277bd;
  margin-top: 50px;
}

/* เอฟเฟกต์ฟองอากาศ */
.bubble {
  position: fixed;
  bottom: -120px;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9), rgba(173,216,230,0.4));
  border-radius: 50%;
  opacity: 0.8;
  box-shadow: 0 0 10px rgba(173,216,230,0.6);
  animation: rise 9s infinite ease-in;
  z-index: 1;
}
@keyframes rise {
  0% { transform: translateY(0) scale(1); opacity: 0.8; }
  100% { transform: translateY(-120vh) scale(1.6); opacity: 0; }
}
</style>

<script>
function createBubbles(){
  for(let i=0;i<15;i++){
    let bubble = document.createElement('div');
    bubble.classList.add('bubble');
    let size = Math.random()*40+20;  
    bubble.style.width = size+'px';
    bubble.style.height = size+'px';
    bubble.style.left = Math.random()*100+'%';
    bubble.style.animationDuration = (8+Math.random()*5)+'s';
    bubble.style.animationDelay = (Math.random()*5)+'s';
    document.body.appendChild(bubble);
    setTimeout(()=>bubble.remove(), 13000);
  }
}
createBubbles();
</script>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("📱Marine Waste AI")
st.sidebar.markdown("---")
st.sidebar.header("👧🏽 About the Developer")
st.sidebar.markdown("""
**ชื่อ:** น.ส.ภัทราวรรณ พรหมเรืองฤทธิ์  
**รหัสนักศึกษา:** 681110071 🎓  

---

**Marine Waste AI** พัฒนาเพื่อช่วยจำแนกประเภทของขยะทะเล  
เช่น พลาสติก โลหะ และเศษขยะชีวภาพอื่น ๆ  
โดยใช้โมเดล AI ที่ฝึกจาก Roboflow  

🌊 **เป้าหมาย:**  
- สร้างความตระหนักรู้เกี่ยวกับปัญหามลพิษทางทะเล  
- ใช้เทคโนโลยี AI เพื่อสนับสนุนการอนุรักษ์สิ่งแวดล้อม  

---

💻 Powered by [Streamlit](https://streamlit.io) & [Roboflow](https://roboflow.com)
""")

# ส่วนหลัก
st.title("🌊 Marine Waste AI")
st.write("อัปโหลดภาพเพื่อให้ AI จำแนกประเภทของขยะทะเลอย่างชาญฉลาด")

uploaded = st.file_uploader("📤 เลือกรูปภาพ", type=["jpg", "jpeg", "png"])

# Roboflow API
API_KEY = "TCwrOT5oJu5pTNpnNKSV"
MODEL_PATH = "marine-waste-ai-wb2eb/3"
ENDPOINT = f"https://classify.roboflow.com/{MODEL_PATH}?api_key={API_KEY}"

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="📸 ภาพที่อัปโหลด", use_container_width=True)

    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")

    with st.spinner("🤖 กำลังให้ AI วิเคราะห์..."):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(ENDPOINT, data=b64_img, headers=headers, timeout=60)
        result = resp.json()

    try:
        preds = result.get("predictions", [])
        if isinstance(preds, list) and len(preds) > 0:
            top = max(preds, key=lambda x: x.get("confidence", 0))
            pred_class = top["class"]
            confidence = top["confidence"] * 100

            st.markdown(f"""
            <div class="result-box">
            <h3>✅ ผลลัพธ์การวิเคราะห์</h3>
            <p><b>ประเภทของขยะ:</b> {pred_class}</p>
            <p><b>ความมั่นใจของ AI:</b> {confidence:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(confidence / 100)
        else:
            st.error("ไม่พบผลลัพธ์จากโมเดล")
    except Exception:
        st.error("⚠️ เกิดข้อผิดพลาดในการประมวลผล")

# Footer
st.markdown("""
<footer>
💻 Powered by <a href="https://streamlit.io" target="_blank">Streamlit</a> & 
<a href="https://roboflow.com" target="_blank">Roboflow</a> | Marine Waste AI 🌊
</footer>
""", unsafe_allow_html=True)
