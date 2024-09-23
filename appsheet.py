import streamlit as st
from calculation import form, input_form,  save_to_excel, crin, update_crin_table, insert_ocr_data, processing, update_processing_table, input_form_processing, color, delete_selected_rows
from database import show_data
from streamlit_option_menu import option_menu
import pandas as pd

st.set_page_config(page_icon=None, layout="wide")

#UI Goes here
@st.fragment
def home():
    with st.container(height=750, border=True):
        A1, A2, A3 = st.columns([5, 3, 1])
        with A1:
            st.header("Cold Store Data")
        with A2:
            with st.expander("choose"):
                a = st.button("Add")
                delect_button = st.button("delete", key="delete")
                if a:
                    input_form()

        with A3:
            pass

        if "crin_data" not in st.session_state:
            st.session_state.crin_data = crin()
        switch = st.toggle("open editor mode", key="Cold")
        if switch:
            save_button = st.button("save", key="save-col2")
            new_data = st.data_editor(st.session_state.crin_data, use_container_width=True, key="data-1", height=500)
            if save_button:
                update_crin_table(new_data)
            elif delect_button:
                delete_selected_rows(new_data, 'crin')
        else:
            new_data = st.dataframe(st.session_state.crin_data, use_container_width=True, height=500, key="Not")

@st.fragment
def home_right():
    with st.container(border=True, height=750):
        B1, B2, B3 = st.columns([5, 3, 1])
        with B1:
            st.header("Processing Data")
        with B2:
            with st.expander("choose"):
                a = st.button("Add", key="B")
                delete = st.button("Delete", key="delete2")
                if a:
                    input_form_processing()
        with B3:
            pass

        b = processing()
        on = st.toggle("Open Editor Mode")
        if on:
            st.toast("Editor Mode Opened")
            buton = st.button("save", key="save")
            new_data = st.data_editor(b, use_container_width=True, height=500, hide_index=True)

            if buton:
                update_processing_table(new_data)
            elif delete:
                delete_selected_rows(new_data, 'processing')
        else:
            style_df = b.style.applymap(color, subset=["Total_Mc", "Total_Kg"])
            new_data = st.dataframe(style_df, use_container_width=True, height=500, hide_index=True)

selected2 = option_menu("Welcome To MSL", ["Home", "Upload", "Tasks", 'Settings'],
    icons=['house', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000000!important"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "secondary"},
    }
)
if selected2 == "Home":
    # dashboard tab
    with st.sidebar:
        with st.container(border=True):
            form()
    col2, col3 = st.columns([5, 5])

    with col2:
        home()

    with col3:
        home_right()