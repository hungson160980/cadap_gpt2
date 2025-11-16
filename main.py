# main.py
import streamlit as st
from src.ui.components import sidebar_api_input, layout_tabs
from src.logic.parser_docx import parse_docx_streamlit
from src.logic.finance import recalc_all
from src.export.export_excel import export_schedule_excel
from src.export.export_docx import export_docx
from src.ai.gemini_client import GeminiClient

st.set_page_config(page_title="Thẩm định vay vốn", layout="wide")

api_key = sidebar_api_input()
uploaded = st.file_uploader("Upload file .docx (Phương án sử dụng vốn)", type=["docx"])

if "data" not in st.session_state:
    st.session_state.data = None

if uploaded:
    st.session_state.data = parse_docx_streamlit(uploaded)
    st.success("Đã đọc file DOCX và trích xuất (nếu có dữ liệu).")

if st.session_state.data is None:
    st.info("Chưa upload file, dùng dữ liệu mẫu")
    st.session_state.data = {
        "identification":{"ten":"Nguyễn Văn Minh","cccd":"001085012345","dia_chi":"Bắc Ninh","phone":"0900000000"},
        "finance":{"muc_dich":"Mua nhà","tong_nhu_cau":5000000000,"von_doi_ung":1000000000,"so_tien_vay":5000000000,"lai_suat_p_a":8.5,"thoi_han_thang":60},
        "collateral":[{"loai":"BĐS","gia_tri":6000000000,"dia_chi":"Lô 45","ltv_percent":80}],
        "income":{"thu_nhap_hang_thang":100000000,"chi_phi_hang_thang":45000000}
    }

layout_tabs(st.session_state.data, recalc_callback=lambda: recalc_all(st.session_state))

st.markdown("---")
st.header("Xuất File")

if st.button("Xuất Excel kế hoạch trả nợ"):
    df = recalc_all(st.session_state)
    data = export_schedule_excel(df)
    st.download_button("Tải Excel", data=data, file_name="ke_hoach_tra_no.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if st.button("Xuất báo cáo DOCX"):
    b = export_docx(st.session_state.data)
    st.download_button("Tải báo cáo.docx", data=b, file_name="bao_cao.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# AI area (stub)
if api_key:
    client = GeminiClient(api_key)
    q = st.sidebar.text_area("Chat cùng Gemini")
    if st.sidebar.button("Gửi"):
        st.sidebar.write(client.chat(q))
