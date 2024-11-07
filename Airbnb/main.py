import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from io import BytesIO

# Streamlit app title
st.title("Airbnb Data Scraper")

# Step 1: Upload an Excel file
uploaded_file = st.file_uploader("Upload your Excel file with Airbnb links", type="xlsx")
if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file)
    limit_time = 'August 2024'

    # Initialize variables
    Table = pd.DataFrame()

    # Step 2: Initiate Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    # Loop through links in the Excel file
    for idx, link in enumerate(df.Link):
        Autore = []
        Sentimento = []
        Durata_pernottamento = []
        Data_commento = []
        Testo_commento = []
        Info_addizionali = []

        driver.get(link)
        time.sleep(5)
        counter = 0
        while True:
            try:
                counter += 1
                dialog = driver.find_element(By.CLASS_NAME, '_17itzz4')
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dialog)
                time.sleep(3)
                elements = driver.find_elements(By.CLASS_NAME, '_1tqgvho')
                full_text = elements[0].text
                if str(limit_time) in full_text or counter > 5:
                    break
            except:
                time.sleep(5)
                pass
        
        # Parsing text data
        full_text_list = []
        for f in full_text.split('\n,\n·\n'):
            for s in f.split('\n'):
                full_text_list.append(s)

        for i, r in enumerate(full_text_list):
            if 'Rating, ' in str(r) and ' stars' in str(r):
                try: Autore.append(full_text_list[i-2])
                except: Autore.append(None)
                try: Info_addizionali.append(full_text_list[i-1])
                except: Info_addizionali.append(None)
                try: Sentimento.append(full_text_list[i])
                except: Sentimento.append(None)
                try: Data_commento.append(full_text_list[i+1])
                except: Data_commento.append(None)
                try: Durata_pernottamento.append(full_text_list[i+2])
                except: Durata_pernottamento.append(None)
                try: Testo_commento.append(full_text_list[i+3])
                except: Testo_commento.append(None)

        # Creating a DataFrame for the scraped data
        table = pd.DataFrame({
            'Autore': Autore,
            'Sentimento': Sentimento,
            'Durata_pernottamento': Durata_pernottamento,
            'Data_commento': Data_commento,
            'Testo_commento': Testo_commento,
            'Info_addizionali': Info_addizionali,
            'Property': str(df['Property'][idx]),
            'link': link
        })

        Table = pd.concat([Table, table])
        st.write(f"Property {idx} is now completed")

    # Closing the Selenium driver
    driver.quit()

    # Final DataFrame formatting
    Table = Table[['Property', 'link', 'Autore', 'Sentimento', 'Durata_pernottamento',
                   'Data_commento', 'Testo_commento', 'Info_addizionali']]

    # Step 3: Download as Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        Table.to_excel(writer, index=False, sheet_name='Airbnb Data')
    output.seek(0)

    st.download_button(
        label="Download Excel File",
        data=output,
        file_name="Air_bnb_test_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
