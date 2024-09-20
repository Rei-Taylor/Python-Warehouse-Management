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

@st.dialog("Enter New Entries")
def input_form():
    connect = sql()
    input_1 = st.text_input("Sr_No")
    input_2 = st.text_input("Fi_No")
    input_3 = st.date_input("Date")
    input_4 = st.text_input("Company")
    input_5 = st.text_input("Item")
    input_6 = st.text_input("Type")
    input_7 = st.text_input("Size")
    input_8 = st.text_input("Conversion")
    input_9 = st.text_input("Total_Mc")
    
    input_11 = st.text_input("Freezing_Type")

    a = st.button("Save")
    if a:
        add_row(connect, input_1,input_2,input_3,input_4,input_5,input_6,input_7,input_8,input_9,multiply(input_8,input_9),input_11)
        st.success("new row added")

def crin():
    connect = sql()
    df = show_crin(connect)
    return df
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