import streamlit as st
import pandas as pd
from database import connect_to_db,show_data, add_user, update_user



path = r"C:\Users\User\Downloads\MSLI_TEST_CRIN (7).xlsx"
a = "root"
b = "TotsukaSaika217"
c = "localhost"
d = 3306
e = "msl"

@st.cache_resource
def sql():
    return connect_to_db(a, b, c, d, e)



@st.cache_data
def sheet_name():
    a = pd.ExcelFile(path)
    sn = a.sheet_names
    return sn


@st.cache_data
def datasource(sn):
    df = pd.read_excel(path, sn)
    return df

def form():
    st.header("You Can Filter Here")
    input_1 = st.text_input("Company", key=1)
    input_2 = st.text_input("Item", key=2)
    input_3 = st.text_input("Size", key=3)
    input_4 = st.date_input("date", key=4)
    input_5 = st.text_input("size", key=5)

    a = st.button("search", on_click=lambda:print("button clicked"), key="form_button")


@st.dialog("Enter New Entries")
def input_form():    
    input_1 = st.text_input("Company")
    input_2 = st.text_input("Item")
    input_3 = st.text_input("Size")
    input_4 = st.date_input("date")
    input_5 = st.text_input("size")

    a = st.button("Save", on_click=lambda:print("button clicked"))

#sqlconnection
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

def update(new_data):
    session = sql()
    for index, row in new_data.iterrows():
        update_user(session, row['ID'], row['Name'], row['Age'])
    st.success("Database updated")



        




if __name__ == "__main__":
    connect = connect_to_db(a, b, c, d, e) 
