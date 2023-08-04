
# Import the needed libraries
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import psycopg2
import json

#Configure Layout

st.set_page_config(
    page_title = 'Crime in Germany', 
    page_icon = '👮', 
    layout = "wide", # or 'centered'
    initial_sidebar_state = "auto", #"collapsed"
    menu_items = {'About':'''Capstone Project from neuefische Bootcamp.  
                  Johanna Köpke, Julie Laur & Alexander Schuppe.'''}
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 0rem;
                    padding-left: 2.5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Configure Variables
if 'year' not in st.session_state:
    st.session_state['year'] = 2022



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

# Show the input field for the password
if 'logged_in' not in st.session_state:
    # The very first run of the app, no password entered yet
    st.session_state['logged_in'] = False
    st.text_input('Password', type='password', on_change=check_password, key='password')
elif not st.session_state['logged_in']:
    # User has input wrong password
    st.text_input('Password', type='password', on_change=check_password, key='password')
    st.error('🧐 Wrong Password')

# Remove after end of development and uncomment upper block
# st.session_state['logged_in'] = True



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
    

    


    col1, col2 = st.columns([0.35, 0.65])

    with col1:
        # Load needed Dataframe and show table
        query = '''
            select bundesland, anzahl_erfasste_faelle, year
            from public.laender_grund_2022_until_2018
            where schluessel = '------'
            and bundesland != 'Bundesrepublik Deutschland'
            and year = '2022';
        '''
        df_crimes_bundeslaender = get_dataframe(query)
        df_crimes_bundeslaender.columns = ['State', 'Cases', 'Year']
        st.write(df_crimes_bundeslaender)

    with col2:
        # Make Bar-Chart from Dataframe
        fig = px.bar(
            df_crimes_bundeslaender,
            x = df_crimes_bundeslaender['State'],
            y = df_crimes_bundeslaender['Cases'],
            hover_name = 'State',
            hover_data = {'State':False},
            # labels = {'bundesland':'State', 'anzahl_erfasste_faelle':'Crimes'},
            title = 'Crimes per State in 2022'
        )
        fig.update_xaxes(tickangle=-90)
        # fig.show()
        st.plotly_chart(fig)

    # Make Map for german states
    # Load Geo-Data for states
    with open('data/bundeslaender_polygons.json') as response:
        geo_data = json.load(response)
    # Create Map
    fig2 = px.choropleth(
        df_crimes_bundeslaender, # Crime data
        locations = 'State', #column in dataframe
        geojson = geo_data, #geodata in geoJSON format
        featureidkey = 'properties.NAME_1', #key that merges to dataframe
        color = 'Cases', #in dataframe
        # labels = {'bundesland':'State', 'anzahl_erfasste_faelle':'Crimes'},
        hover_name = 'State',
        hover_data = {'State':False},
        title = 'Crime in Germany',
    )
    fig2.update_geos(fitbounds='locations', visible=False)
    #fitbounds: zoomt in die Karte, 
    #visible:False blendet alles andere von der Karte aus
    st.plotly_chart(fig2)

    
    with st.sidebar:
        st.subheader('Dashboard Controls')
        st.session_state['year'] = st.slider('🗓 Year', min_value=2018, max_value=2022, value=2022)
        state = st.selectbox('🇩🇪 State', df_crimes_bundeslaender['State'])
        gender = st.radio('☯️ Gender', ['All', 'Female', 'Male'])
        st.button('☀️ Reset')
        st.divider()
        st.markdown('#### 👋 Interested in us?')
        st.image('img/linkedin.png', width=20)
        st.markdown('''Johanna Köpke  
                    [Julie Laur](https://www.linkedin.com/in/julie-laur-a4167713a/)  
                    ![](img/linkedin.png) [Alexander Schuppe](https://www.linkedin.com/in/alexander-schuppe/)  ''')
        st.divider()
        st.caption('Impressum')
    

    st.subheader(f"Crime in Germany {st.session_state['year']}")
    st.markdown('#### Distribution and Frequency Development')
    st.divider()

