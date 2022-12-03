import streamlit
import pandas as pd
import requests
from urllib.error import URLError
import snowflake.connector

streamlit.title('My parents New Healthy Diner')
streamlit.header('Breakfast    Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach &  Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avcado Toast')


########################################################################################################################
#######################CSV FILE FROM S3 AS FRUIT LIST################pandas and streamlit used
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas as pd
my_fruit_list= pd.read_csv(r"https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
# Every multi select default values you give must be in list
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#######################################################################################################################
#####################   FRUITYVICE FRUIT ADVICE..USER ADDS IN INPUT VALUES..GET REQUEST TO FRUITY VICE API ##########
# REPONSE IN THE FORM OF JSON..NO KEY REQUIRED #################REQUEsts library used
#New section to display fruityivice api response 

streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information") 
    else:
         fruityvice_response = requests.get(f"https://www.fruityvice.com/api/fruit/{fruit_choice}")
         fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
         streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
     
#######################################################################################################################
####################### CONNECTING TO SNOWFLAKE USING STREAMLIT SECRETS[TOML FORMAT]..CURSOR CREATION..USING 
#### THAT CURSOR .EXECUTE SQL STATEMENTS..FETCH VALUES FROM CURSOR OUTPUT IT TO STREAMLIT TO DISPLAY IN THE FORM OF DATAFRAME

#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
xyz = my_cur.execute("select * from fruit_load_list")
my_data_row = xyz.fetchall()
streamlit.header("fruit load list contains:")
streamlit.dataframe(my_data_row)
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_data_row))
my_cur.execute("insert into fruit_load_list values('from streamlit')")






