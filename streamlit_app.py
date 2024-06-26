# Import python packages
import requests
import pandas
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your Smoothie :balloon:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your Smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()        

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop() 
ingredients_list =st.multiselect('choose upto 5 ingredients:', my_dataframe , max_selections=5)

#st.success('Your Smoothie is ordered!', icon="✅")

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
            ingredients_string += fruit_choosen + ' '

            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen , 'SEARCH_ON'].iloc[0]
            #st.write('The search value for ' ,fruit_choosen , ' is ' , search_on , '.') 
            st.subheader(fruit_choosen + ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
            fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)


        
        
