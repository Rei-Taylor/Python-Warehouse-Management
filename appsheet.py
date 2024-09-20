import streamlit as st
from calculation import datasource, sheet_name, form, input_form, data, input_user, update, save_to_excel, crin, update_crin_table, insert_ocr_data
from database import show_data

st.set_page_config(page_icon=None, layout="wide")

st.header("Welcome to MSL")
with st.container(height=54):
    st.markdown("<div class=container>Welcome To MSL</div>", unsafe_allow_html=True)

# dashboard tab
with st.sidebar:
    with st.container(border=True):
        form()
col2, col3 = st.columns([8, 2])

with col2:
    with st.container(height=750, border=True):
        A1, A2, A3 = st.columns([5, 3, 1])
        with A1:
            pass
        with A2:
            with st.expander("choose"):
                a = st.button("Add")
                if a:
                    input_form()
        with A3:
            pass
        
        b = crin()
        print(b)
        save_button = st.button("save", key="save-col2")
        new_data = st.data_editor(b, use_container_width=True, key="data-1")
        if save_button:
            update_crin_table(new_data)

        # Add OCR functionality
        st.subheader("OCR Scan")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            ocr_button = st.button("Process OCR and Insert Data")
            if ocr_button:
                insert_ocr_data(uploaded_file)

with col3:
    with st.container(border=True):
        B1, B2, B3 = st.columns([5, 3, 1])
        with B1:
            pass
        with B2:
            with st.expander("choose"):
                a = st.button("Add", key="B")
                if a:
                    input_user()
        with B3:
            pass
        a = st.selectbox("Choose DataSource", sheet_name(), key="table-2")
        if a:
            b = data()
            buton = st.button("save", key="save")
            new_data = st.data_editor(b, use_container_width=True)
            if buton:
                update(new_data)