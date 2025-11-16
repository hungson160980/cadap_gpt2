import re
from docx import Document

def parse_docx_streamlit(f):
    doc = Document(f)
    txt = "\n".join(p.text for p in doc.paragraphs)
    # Basic heuristics; extend as needed for specific templates
    identification = {}
    finance = {}
    collateral = []
    income = {}

    m = re.search(r"Họ và tên[:\s]*([A-Za-zÀ-ỹ\s0-9]+)", txt)
    if m:
        identification['ten'] = m.group(1).strip()
    else:
        identification['ten'] = ''

    m = re.search(r"CMND|CCCD[:\s]*([0-9]{9,12})", txt)
    if m:
        identification['cccd'] = m.group(1)
    else:
        identification['cccd'] = ''

    identification['dia_chi'] = ''
    identification['phone'] = ''

    finance['muc_dich'] = ''
    finance['tong_nhu_cau'] = 0
    finance['von_doi_ung'] = 0
    finance['so_tien_vay'] = 0
    finance['lai_suat_p_a'] = 8.5
    finance['thoi_han_thang'] = 60

    collateral.append({'loai':'BĐS','gia_tri':0,'dia_chi':'','ltv_percent':0.0})
    income['thu_nhap_hang_thang'] = 0
    income['chi_phi_hang_thang'] = 0

    return {'identification':identification,'finance':finance,'collateral':collateral,'income':income}
