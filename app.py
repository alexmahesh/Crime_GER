
# Import the needed libraries
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import folium_static
import psycopg2

st.set_page_config(
    page_title = 'Crime in Germany', 
    page_icon = '👮', 
    layout = "wide", # or 'centered'
    initial_sidebar_state = "auto", 
    menu_items = {'About':'''Capstone Project from neuefische Bootcamp.  
                  Johanna Köpke, Julie Laur & Alexander Schuppe.'''}
)


# Protect Dashboard with a simple password mechanism
def check_password():
    '''
    Checks if the entered password is correct or wrong.
    If the password is correct, the user is logged-in, 
    otherwise he/she is not, which is stored in a session
    variable.
    '''
    if st.session_state['password'] == st.secrets['dashboard_password']:
        st.session_state['logged_in'] = True
    else:
        st.session_state['logged_in'] = False
    del st.session_state['password'] # delete entered password

# # Show the input field for the password
# if 'logged_in' not in st.session_state:
#     # The very first run of the app, no password entered yet
#     st.session_state['logged_in'] = False
#     st.text_input('Password', type='password', on_change=check_password, key='password')
# elif not st.session_state['logged_in']:
#     # User has input wrong password
#     st.text_input('Password', type='password', on_change=check_password, key='password')
#     st.error('🧐 Wrong Password')

# Remove after end of development and uncomment upper block
st.session_state['logged_in'] = True



# ---------------------------------
# --- Here starts the Dashboard ---
#     Only visible after log-in
# ---------------------------------
if st.session_state['logged_in']:
    

    @st.cache_data
    def get_dataframe(query):
        '''
        Make a query in the database and
        return the result as a pandas dataframe.
        '''
        con = psycopg2.connect(
            host = st.secrets.azure_db['host'],
            port = st.secrets.azure_db['port'],
            database = st.secrets.azure_db['database'],
            user = st.secrets.azure_db['user'],
            password = st.secrets.azure_db['password']
        )
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        con.close()
        return pd.DataFrame(result)
    

    # query = 'select * from public.bund_grund_2022_until_2018 LIMIT 10'
    # df_grund_bund = get_dataframe(query)
    # df_grund_bund


    query = '''
        select schluessel, straftat, bundesland, anzahl_erfasste_faelle, year
        from public.laender_grund_2022_until_2018
        where schluessel = '------'
        and bundesland != 'Bundesrepublik Deutschland';
    '''
    df_crimes_bundeslaender = get_dataframe(query)
    df_crimes_bundeslaender.columns = ['schluessel', 'straftat', 'bundesland', 'anzahl_erfasste_faelle', 'year']
    
    
    df_map_bundeslaender = gpd.read_file('data/bundeslaender.json')
    df_map_bundeslaender.rename(columns={'GEN':'bundesland'}, inplace=True)
    

    df_map_crimes_bundeslaender = df_map_bundeslaender.merge(df_crimes_bundeslaender, on='bundesland')
    df_tmp = df_map_crimes_bundeslaender[df_map_crimes_bundeslaender['year']=='2022']
    st.write(df_tmp.head(2))

    
    

    m = folium.Map(
        location = [52.52, 13.4],
        tiles = 'OpenStreetMap', # 'CartoDB positron'
        zoom_start = 6,
    )

    folium.Marker(
        [52.52, 13.4],
        popup = "Berlin",
        tooltip = 'Click me',
        icon = folium.Icon(color='red', icon = 'info-sign')
    ).add_to(m)
        
    folium_static(m, width=900, height=550)