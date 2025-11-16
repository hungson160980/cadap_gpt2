import streamlit as st
from src.logic.finance import recalc_all

def sidebar_api_input():
    return st.sidebar.text_input("Gemini API Key (nếu có)", type="password")

def layout_tabs(data, recalc_callback):
    tabs = st.tabs(["Định danh","Tài chính","TSĐB","Dòng tiền","Biểu đồ"])
    with tabs[0]:
        st.header("Thông tin định danh")
        idf = data.get("identification", {})
        idf["ten"] = st.text_input("Họ và tên", idf.get("ten",""))
        idf["cccd"] = st.text_input("CCCD/CMND", idf.get("cccd",""))
        idf["dia_chi"] = st.text_area("Địa chỉ", idf.get("dia_chi",""))
        idf["phone"] = st.text_input("Số điện thoại", idf.get("phone",""))
        data["identification"] = idf

    with tabs[1]:
        st.header("Thông tin tài chính")
        fin = data.get("finance", {})
        fin["muc_dich"] = st.text_input("Mục đích vay", fin.get("muc_dich",""))
        fin["tong_nhu_cau"] = st.number_input("Tổng nhu cầu vốn (đồng)", value=fin.get("tong_nhu_cau",0), step=1000000, format="%d")
        fin["von_doi_ung"] = st.number_input("Vốn đối ứng (đồng)", value=fin.get("von_doi_ung",0), step=1000000, format="%d")
        fin["so_tien_vay"] = st.number_input("Số tiền vay (đồng)", value=fin.get("so_tien_vay",0), step=1000000, format="%d")
        fin["lai_suat_p_a"] = st.number_input("Lãi suất (%/năm)", value=fin.get("lai_suat_p_a",8.5), step=0.1, format="%.2f")
        fin["thoi_han_thang"] = st.number_input("Thời hạn (tháng)", value=fin.get("thoi_han_thang",60), step=1)
        data["finance"] = fin

    with tabs[2]:
        st.header("Tài sản bảo đảm")
        coll = data.get("collateral", [])
        for i, c in enumerate(coll):
            st.subheader(f"Tài sản #{i+1}")
            c["loai"] = st.text_input(f"Loại tài sản #{i+1}", value=c.get("loai",""))
            c["gia_tri"] = st.number_input(f"Giá trị (đồng) #{i+1}", value=c.get("gia_tri",0), step=1000000, format="%d")
            c["dia_chi"] = st.text_input(f"Địa chỉ #{i+1}", value=c.get("dia_chi",""))
            c["ltv_percent"] = st.number_input(f"LTV (%) #{i+1}", value=c.get("ltv_percent",0.0), step=0.1, format="%.2f")
        if st.button("Thêm tài sản"):
            coll.append({"loai":"","gia_tri":0,"dia_chi":"","ltv_percent":0.0})
        data["collateral"] = coll

    with tabs[3]:
        st.header("Kết quả tính toán")
        df = recalc_callback()
        st.write("Tổng quan:")
        summary = st.session_state.get("summary", {})
        st.write("Thanh toán hàng tháng:", summary.get("monthly_payment",0))
        st.write("DSR (%):", f"{summary.get('dsr_percent'):.2f}%" if summary.get("dsr_percent") else "Không có dữ liệu")
        st.write("LTV (%):", f"{summary.get('ltv_percent'):.2f}%" if summary.get("ltv_percent") else "Không có dữ liệu")
        st.subheader("Lịch trả nợ (một vài dòng)")
        st.dataframe(df.head(12))

    with tabs[4]:
        st.header("Biểu đồ trả nợ")
        import matplotlib.pyplot as plt
        df = recalc_callback()
        if not df.empty:
            fig, ax = plt.subplots()
            ax.plot(df['month'], df['payment'])
            ax.set_xlabel('Tháng')
            ax.set_ylabel('Số tiền (đồng)')
            st.pyplot(fig)
