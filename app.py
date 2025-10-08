import streamlit as st
from PIL import Image
import io, base64, requests, json

#หน้าเว็บ
st.set_page_config(page_title="🌊 Marine Waste AI", page_icon="🌊", layout="wide")

#สี
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(to bottom, #e0f7fa, #ffffff);
}
[data-testid="stSidebar"] { background-color: #b3e5fc; }
h1, h2, h3, h4, h5 { color: #01579b; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌐 Marine Waste AI")
st.sidebar.header("📘 About the Developer")
st.sidebar.markdown("""
**น.ส.ภัทราวรรณ พรหมเรืองฤทธิ์**   
รหัสนักศึกษา **681110071**

โครงการใช้ AI จำแนกประเภทขยะทะเล เพื่อสนับสนุนการอนุรักษ์สิ่งแวดล้อม
""")

st.title("🌊 Marine Waste AI")
st.write("อัปโหลดภาพเพื่อให้ AI จำแนกประเภทของขยะทะเล")

#ค่าคงที่ของ Roboflow
API_KEY = "TCwrOT5oJu5pTNpnNKSV" 
MODEL_PATH = "marine-waste-ai-wb2eb/3"  
ENDPOINT = f"https://classify.roboflow.com/{MODEL_PATH}?api_key={API_KEY}"  # docs: classify.roboflow.com

#อัปโหลดและเรียก API
uploaded = st.file_uploader("📤 เลือกรูปภาพ", type=["jpg", "jpeg", "png"])
if uploaded:
    #แสดงภาพ
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="ภาพที่อัปโหลด", use_container_width=True)

    #แปลงภาพ -> base64 ตามสเปค Roboflow Classification API
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")

    with st.spinner("🔍 กำลังวิเคราะห์..."):
        #ส่งเป็น x-www-form-urlencoded (ตัว body คือสตริง base64)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(ENDPOINT, data=b64_img, headers=headers, timeout=60)
        resp.raise_for_status()
        result = resp.json()

    #รองรับทั้งรูปแบบผลลัพธ์แบบ list และ dict ตามเอกสาร
    #(Single-label อาจคืนเป็น list, หรือเป็น dict + predicted_classes)
    pred_text = ""
    try:
        #กรณี list
        preds = result.get("predictions", [])
        if isinstance(preds, list) and preds:
            top = max(preds, key=lambda x: x.get("confidence", 0))
            pred_text = f"{top['class']} ({top['confidence']*100:.2f}%)"
        else:
            #กรณี dict
            preds_dict = result.get("predictions", {})
            if isinstance(preds_dict, dict) and preds_dict:
                #เลือก class ที่ confidence สูงสุด
                top_class = max(preds_dict.items(), key=lambda kv: kv[1].get("confidence", 0))[0]
                conf = preds_dict[top_class]["confidence"] * 100
                pred_text = f"{top_class} ({conf:.2f}%)"
    except Exception:
        pred_text = "ไม่สามารถอ่านผลลัพธ์ได้"

    if pred_text:
        st.success(f"✅ ผลลัพธ์: **{pred_text}**")
    else:
        st.error("ไม่พบผลลัพธ์จากโมเดล")

    # Debug ปุ่มดู JSON ดิบ (เผื่ออาจารย์อยากเห็น)
    with st.expander("ดูผลลัพธ์แบบ JSON"):
        st.code(json.dumps(result, ensure_ascii=False, indent=2))
