import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host='localhost', #misalnya "localhost"
        user='root',
        password='',
        database='db_dal'
    )
    return connection

def get_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM pddikti_example"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Judul aplikasi
st.title('Streamlit Simple App')

# Menambahkan navigasi di sidebar
page = st.sidebar.radio("Pilih halaman", ["Dataset", "Visualisasi", "Form Input"])

if page == "Dataset":
    st.header("Halamat Dataset")

    # Baca file CSV
    data = get_data_from_db()

    # Tampilkan data di streamlit
    st.write(data)


elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Baca file CSV
    data = pd.read_csv("pddikti_example.csv")

    #Filter berdasarkan universitas
    selected_university = st.selectbox('Pilih Universitas', data['universitas'].unique())
    filtered_data = data[data['universitas']== selected_university]

    #Buat visualisasi
    plt.figure(figsize=(12, 6))

    for prog_studi in filtered_data['program_studi'].unique():
        subset = filtered_data[filtered_data['program_studi']== prog_studi]

        # Urutkan data berdasarkan "id" dengan urutan menurun
        subset = subset.sort_values(by="id", ascending=False)

        plt.plot(subset['semester'], subset['jumlah'], label=prog_studi)

    plt.title(f"visualisasi data untuk {selected_university}")
    plt.xlabel('Semester')
    plt.xticks(rotation=90) # Rotasi label sumbu x menjadi vertikal
    plt.ylabel("Jumlah")
    plt.legend()

    st.pyplot()   
