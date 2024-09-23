import streamlit as st
import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
from database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql://root:TotsukaSaika217@localhost:3306/msl', pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)

path = r"C:\Users\User\Downloads\MSLI_TEST_CRIN (3).xlsx"
a = "root"
b = "TotsukaSaika217"
c = "localhost"
d = 3306
e = "msl"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
Freezing_Types = ["Airblast-G","Airblast-BG","Airblast-W","Contact","Airblast-IQF","Double-Glazing"]

@st.cache_resource
def sql():
    return connect_to_db()

@st.cache_data
def sheet_name():
    a = pd.ExcelFile(path, engine='openpyxl')
    sn = a.sheet_names
    return sn

@st.cache_data
def datasource(sn):
    df = pd.read_excel(path, sheet_name=sn, engine='openpyxl')
    return df

def save_to_excel(df, sheet_name):
    with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    st.success("Data saved to Excel successfully")

def form():
    st.header("You Can Filter Here")
    input_1 = st.text_input("Company", key=1)
    input_2 = st.text_input("Item", key=2)
    input_3 = st.text_input("Size", key=3)
    input_4 = st.date_input("date", key=4)
    input_5 = st.text_input("size", key=5)

    a = st.button("search", on_click=lambda: print("button clicked"), key="form_button")

#other logic here
def multiply(a, b):
    mu = pd.to_numeric(a) * pd.to_numeric(b)
    return mu

def color(val):
    result = 'color: yellow' if val < 100 else ''
    return result

#show here    
def crin():
    connect = sql()
    df = show_crin(connect)
    df['Total_Mc'] = df['Total_Mc'].round(2)
    df['Total_Kg'] = df['Total_Kg'].round(2)
    df['selected'] = False
    return df

def processing():
    connect = sql()
    df = show_processing(connect)
    df['Total_Mc'] = df['Total_Mc'].round(2)
    df['Total_Kg'] = df['Total_Kg'].round(2)
    df['selected'] = False
    return df

#unique values goes here
def unique_values():
    df_crin = crin()
    unique_company = df_crin["Company"].unique()

    select_company = st.selectbox("Company",unique_company)

    filtered_df = df_crin[df_crin["Company"] == select_company]

    unique_item = filtered_df["Item"].unique()

    select_item = st.selectbox("Item", unique_item)

    filtered_df_2 = filtered_df[filtered_df["Item"] == select_item]

    unique_type = filtered_df_2["Type"].unique()

    select_type = st.selectbox("Type",unique_type)

    unique_size = filtered_df_2["Size"].unique()

    select_size = st.selectbox("Size",unique_size)

    return select_company,select_item,select_size,select_type

def unique_company(data):
    df_crin = data
    u_c = df_crin["Company"].unique()
    return u_c

def unique_item(data, company=0):
    df_crin = data
    if company == 0:
        filtered_df = df_crin[df_crin["Company"] == company]
        u_i = filtered_df["Item"].unique()
    else:
        u_i = df_crin["Item"].unique()    
    return u_i

def unique_values_processing():
    df_crin = processing()
    unique_company = df_crin["Company"].unique()

    select_company = st.selectbox("Company",np.append(unique_company, "New Company"))

    filtered_df = df_crin[df_crin["Company"] == select_company]

    unique_item = filtered_df["Item"].unique()

    select_item = st.selectbox("Item", unique_item)

    filtered_df_2 = filtered_df[filtered_df["Item"] == select_item]

    unique_type = filtered_df_2["Type"].unique()

    select_type = st.selectbox("Type",unique_type)

    unique_size = filtered_df_2["Size"].unique()

    select_size = st.selectbox("Size",unique_size)

    return select_company,select_item,select_size,select_type

#form goes here
@st.dialog("Enter New Entries")
def input_form():
    connect = sql()
    input_1 = st.number_input("Sr_No")
    input_2 = st.text_input("Fi_No")
    input_3 = st.date_input("Date")
    new = st.toggle("Register New Item", key="Company")
    if new:
        select_company = st.text_input("Company")
        select_item = st.text_input("Item")
        select_size = st.text_input("Size")
        select_type = st.text_input("Type")
    else:    
        select_company,select_item,select_size,select_type = unique_values()

    input_8 = st.text_input("Conversion")
    input_9 = st.text_input("Total_Mc")
    kg = st.number_input("Total_Kg", value=multiply(input_8, input_9))
    
    input_11 = st.selectbox("Freezing_Type",Freezing_Types)

    a = st.button("Save")
    if a:
        add_row(connect, input_1,input_2,input_3,select_company,select_item,select_size,select_type,input_8,input_9,kg,input_11)
        st.toast("new row added")

@st.dialog("Enter New Entries")
def input_form_processing():
    connect = sql()
    input_1 = st.number_input("Sr_No")
    input_2 = st.text_input("Fi_No")
    input_3 = st.date_input("Date")
    new = st.toggle("Register New Item", key="Company")
    if new:
        select_company = st.text_input("Company")
        select_item = st.text_input("Item")
        select_size = st.text_input("Size")
        select_type = st.text_input("Type")
    else:    
        select_company,select_item,select_size,select_type = unique_values()

    input_8 = st.text_input("Conversion")
    input_9 = st.text_input("Total_Mc")
    kg = st.number_input("Total_Kg", value=multiply(input_8, input_9))
    
    input_11 = st.selectbox("Freezing_Type",Freezing_Types)

    a = st.button("Save")
    if a:
        add_processing_row(connect, input_1,input_2,input_3,select_company,select_item,select_size,select_type,input_8,input_9,kg,input_11)
        st.toast("new row added")          

def update_crin_table(new_data):
    with sql() as session:
        try:
            crin_objects = []
            new_data = new_data.dropna(subset=['ID'])
            for index, row in new_data.iterrows():
                crin = session.query(ColdStoreIn).filter_by(ID=row['ID']).first()
                if crin:
                    crin.Sr_No = row['Sr_No']
                    crin.Fi_No = row['Fi_No']
                    crin.Date = row['Date']
                    crin.Company = row['Company']
                    crin.Item = row['Item']
                    crin.Type = row['Type']
                    crin.Size = row['Size']
                    crin.Conversion = row['Conversion']
                    crin.Total_Mc = row['Total_Mc']
                    crin.Total_Kg = row['Total_Kg']
                    crin.Freezing_Type = row['Freezing_Type']
                    crin_objects.append(crin)
            session.bulk_save_objects(crin_objects)
            session.commit()
            st.toast("Database updated")
        except Exception as e:
            session.rollback()
            st.error(f"An error occurred: {e}")

def update_processing_table(new_data):
    with sql() as session:
        try:
            crin_objects = []
            for index, row in new_data.iterrows():
                crin = session.query(ProcessingIn).filter_by(ID=row['ID']).first()
                if crin:
                    crin.Sr_No = row['Sr_No']
                    crin.Fi_No = row['Fi_No']
                    crin.Date = row['Date']
                    crin.Company = row['Company']
                    crin.Item = row['Item']
                    crin.Type = row['Type']
                    crin.Size = row['Size']
                    crin.Conversion = row['Conversion']
                    crin.Total_Mc = row['Total_Mc']
                    crin.Total_Kg = row['Total_Kg']
                    crin.Freezing_Type = row['Freezing_Type']
                    crin_objects.append(crin)
            session.bulk_save_objects(crin_objects)
            session.commit()
            st.toast("Database updated")
        except Exception as e:
            session.rollback()
            st.error(f"An error occurred: {e}")

def delete_selected_rows(df, table):
    with sql() as session:
        try:
            selected_rows = df[df['selected'] == True]
            for index, row in selected_rows.iterrows():
                if table == 'crin':
                    session.query(ColdStoreIn).filter_by(ID=row['ID']).delete()
                elif table == 'processing':
                    session.query(ProcessingIn).filter_by(ID=row['ID']).delete()
            session.commit()
            st.toast("Selected rows deleted")
        except Exception as e:
            session.rollback()
            st.error(f"An error occurred: {e}")

def show_crin_data():
    df = crin()
    edited_df = st.data_editor(df, use_container_width=True)
    if st.button("Delete Selected Rows"):
        delete_selected_rows(edited_df, 'crin')
        st.experimental_rerun()  # Refresh the page to show updated data

def show_processing_data():
    df = processing()
    edited_df = st.data_editor(df, use_container_width=True)
    if st.button("Delete Selected Rows"):
        delete_selected_rows(edited_df, 'processing')
        st.experimental_rerun()  # Refresh the page to show updated data

def ocr_scan(image_path):
    """
    Perform OCR on the given image and return the extracted text.
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def process_ocr_data(text):
    """
    Process the OCR text and convert it into a format suitable for database insertion.
    """
    # Example processing logic, adjust according to your OCR text format
    lines = text.split('\n')
    data = []
    for line in lines:
        if line.strip():
            data.append(line.split())  # Assuming space-separated values
    return data

def insert_ocr_data(image_path):
    """
    Perform OCR on the image and insert the data into ColdStoreIn table.
    """
    text = ocr_scan(image_path)
    data = process_ocr_data(text)
    connect = sql()
    for row in data:
        # Adjust the parameters according to your table schema
        insert_coldstorein(connect, *row)
    st.success("OCR data inserted into ColdStoreIn table")    

if __name__ == "__main__":
    scan = ocr_scan(r"C:\Users\User\Desktop\FastApi\datra.png")
    text = process_ocr_data(scan)
