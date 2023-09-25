import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

def get_connection():
    connection =mysql.connector.connect(host='localhost', user='root', password='', database ='db_dal')
    return connection

def get_data_from_db ():
    conn = get_connection()
    query = "SELECT * FROM pddikti_example"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
#Judul Aplikasi
st.title('Streamlit Simple App')

#Menambahkan Navigasi di Sidebar
page = st.sidebar.radio("Pilih halaman", ["Dataset", "Visualisasi", "Form Input"])



if page == "Dataset":
    st.header("Halaman Dataset")

    #Baca File CSV
    #data = pd.read_csv("pddikti_example.csv")

    #Ubah Menjadi
    data = get_data_from_db()

    #Tampilkan data di streamlit
    st.write(data)

elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Baca file CSV
    #data = pd.read_csv ("pddikti_example.csv")

    data = get_data_from_db()

    #Filter berdasarkan universitas
    selected_university = st.selectbox('Pilih Universitas', data['universitas'].unique())
    filtered_data =data[data["universitas"]== selected_university]

    #Buat Visualisasi
    plt.figure(figsize=(12,6))

    for prog_studi in filtered_data['program_studi'].unique():
        subset = filtered_data[filtered_data['program_studi'] == prog_studi]

        #Urutkan data berdasarkan 'id' dengan urutan menurun
        subset = subset.sort_values(by='id', ascending=False)

        plt.plot(subset['semester'], subset['jumlah'], label=prog_studi)

    plt.title(f"Visualisasi Data Untuk {selected_university}")
    plt.xlabel('Semester')
    plt.xticks(rotation=90) #Rotasi label sumbu x menjadi vertikal
    plt.ylabel('Jumlah')
    plt.legend()

    st.pyplot()

elif page == "Form Input":
    st.header("Halaman Form Input")
    with st.form(key='input_form'):
        input_semester = st.text_input('Semester')
        input_jumlah = st.number_input ('Jumlah', min_value=0, format='%d')
        input_program_studi = st.text_input('Program Studi')
        input_universitas = st.text_input ('Universitas')
        submit_button = st.form_submit_button(label='Submit Data')


    if submit_button:
        conn = get_connection()
        cursor = conn.cursor ()
        query = """
        INSERT INTO pddikti_example(semester, jumlah, program_studi, universitas) VALUES (%s, %s, %s, %s) """
        cursor.execute(query, (input_semester, input_jumlah, input_program_studi, input_universitas))
        conn.commit()
        conn.close()
        st.success("Data Successfully submitted to the Database")