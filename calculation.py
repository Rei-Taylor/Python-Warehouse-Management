import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
from database import connect_to_db, show_data, add_user, update_user, add_row, show_crin, update_crin, insert_coldstorein

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
    return connect_to_db(a, b, c, d, e)

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

def multiply(a, b):
    mu = pd.to_numeric(a) * pd.to_numeric(b)
    return mu
    
def crin():
    connect = sql()
    df = show_crin(connect)
    return df

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


@st.dialog("Enter New Entries")
def input_form():
    connect = sql()


    input_1 = st.text_input("Sr_No")
    input_2 = st.text_input("Fi_No")
    input_3 = st.date_input("Date")
    select_company,select_item,select_size,select_type = unique_values()
    input_8 = st.text_input("Conversion")
    input_9 = st.text_input("Total_Mc")
    
    input_11 = st.selectbox("Freezing_Type",Freezing_Types)

    a = st.button("Save")
    if a:
        add_row(connect, input_1,input_2,input_3,select_company,select_item,select_size,select_type,input_8,input_9,multiply(input_8,input_9),input_11)
        st.success("new row added")



# sqlconnection
def data():
    connect = connect_to_db(a, b, c, d, e)
    df = show_data(connect)
    return df

@st.dialog("Input new user")
def input_user():
    connect = sql()
    a = st.text_input("Name")
    b = st.number_input("Age")
    button = st.button("ADD", key="user")
    if button:
        c = add_user(connect, a, b)
        st.success("new user added")

def update_crin_table(new_data):
    session = sql()
    for index, row in new_data.iterrows():
        update_crin(session, row['ID'], row['Sr_No'], row['Fi_No'], row['Date'], row['Company'], row['Item'], row['Type'],row['Size'], row['Conversion'], row['Total_Mc'], row['Total_Kg'], row['Freezing_Type'])
    st.success("Database updated")   

def update(new_data):
    session = sql()
    for index, row in new_data.iterrows():
        update_user(session, row['ID'], row['Name'], row['Age'])
    st.success("Database updated")

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