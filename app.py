
# Import the needed libraries
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import psycopg2


# ---------------------------------
# Layout/Styling
# (Some configurations for Streamlit)
# ---------------------------------
st.set_page_config(
    page_title = 'Juvenile Crime in Germany', 
    page_icon = ':bar_chart:', 
    layout = "wide", # or 'centered'
    initial_sidebar_state = "auto", #"collapsed"
    menu_items = {'About':'''__Juvenile Crime in Germany.__  
                  This Dashboard belongs to our capstone project from the neuefische Data Analyst Bootcamp May 2023.  
                  Johanna Köpke  
                  Julie Laur  
                  Alexander Schuppe  '''}
)

# Reduce space between components on dashboard with CSS
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

# Remove Streamlit Footer
st.markdown("""<style>.appview-container .main footer {visibility: hidden;}</style>""", unsafe_allow_html=True)
# maybe: .reportview-container

# Remove the decoration on top of Streamlit page
st.markdown("""<style>.css-1dp5vir {visibility: hidden;}</style>""", unsafe_allow_html=True)

# ----------------------------------------------------
# Log-in
# (Protect Dashboard with a simple password mechanism)
# ----------------------------------------------------
def check_password():
    '''
    Checks if the entered password is correct or wrong.
    If the password is correct, the user is logged-in and
    can proceed, otherwise he/she is not logged-in 
    and will not see the dashboard. 
    This state is stored in a session variable.
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


# ----------------------------
# Here starts the Dashboard
# (Only visible after log-in)
# ----------------------------
if st.session_state['logged_in']:

    # ---------------------------------
    # Functions
    # ---------------------------------

    @st.cache_data
    def get_dataframe(query):
        '''
        Make a query to the database and
        return the result as a pandas dataframe.
        The result is cached, so if the data is queried
        again without change, it will be loaded from the cache.
        The database credentials are loaded from the internal
        service offered by Streamlit to protect secrets.
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
        df = pd.read_sql(query, con)
        cur.close()
        con.close()
        return df
    

    def reset():
        '''
        Resets the values of all controls of the dashboard.
        '''
        st.session_state['year'] = 2022
        st.session_state['federal_state'] = 'Germany'
        st.session_state['age_group'] = 'All'
        st.session_state['crime_type'] = 'All'
        st.session_state['gender'] = 'All'
    

    def get_df_overview_linechart(crime_type, age_group, gender):
        '''
        Create a table from global table 'df_bund_abs' for making a linechart out of it.
        @crime_type (list of string): The 'schluessel' of different crime types.
        @age_group (string): The name of the column in the database for the filtered age group.
        @gender (string): The gender to filter for.
        @return (pandas.Dataframe): The dataframe to make a linechart from.
        '''
        df_overview_linechart = df_bund_abs[
            (df_bund_abs['schluessel'].isin(crime_type)) &
            (df_bund_abs['sexus'] == gender)
        ][[
            'schluessel', # =crime_type
            'year',
            'sexus',
            'straftat', # =crime_type
        ]]
        # Add the crime_type (=age_group)
        df_overview_linechart[age_group] = df_bund_abs[age_group]
        # Calculate the sum for the crime_type, if there are several 'schluessel'
        df_overview_linechart = df_overview_linechart.groupby('year', as_index=False).sum()

        return df_overview_linechart
    

    def get_df_overview_map(year, crime_type, age_group, gender):
        # 2022, ['------'], 'All', 'All'
        '''
        Create a table from global table 'df_laender_abs' for making a choropleth map out of it.
        @year (int): The year the map should be filtered to.
        @crime_type (list of string): The 'schluessel' of different crime types.
        @age_group (string): The name of the column in the database for the filtered age group.
        @gender (string): The gender to filter for.
        @return (pandas.Dataframe): The dataframe to make a choropleth map from.
        '''
        df_overview_map = df_laender_abs[
            (df_laender_abs['year'] == year) &
            (df_laender_abs['schluessel'].isin(crime_type)) &
            (df_laender_abs['sexus'] == gender)
        ][[
            'bundesland',
            'schluessel', # =crime_type
            'year',
            'sexus',
            'straftat', # =crime_type
        ]]
        # Add the crime_type (=age_group)
        df_overview_map[age_group] = df_laender_abs[age_group]
        # Calculate the sum for the crime_type, if there are several 'schluessel'
        df_overview_map = df_overview_map.groupby(['bundesland', 'year'], as_index=False).sum()

        return df_overview_map
    

    def get_df_overview_pie(year, age_group, gender):
        '''
        Create a table from global table 'df_bund_abs' for making a pie chart out of it.
        @year (int): The year the pie chart should be filtered to.
        @age_group (string): The name of the column in the database for the filtered age group.
        @gender (string): The gender to filter for.
        @return (pandas.Dataframe): The dataframe to make a pie chart from.
        '''

        # Make a list of all crimes for the pie chart
        crimes = [crime for crime in crime_types.values()] #use the global variable
        crimes = sum(crimes, []) #flatten the list of lists of schluessel
        crimes.remove('------')

        df_overview_pie = df_bund_abs[
            (df_bund_abs['year'] == year) &
            (df_bund_abs['sexus'] == gender) &
            (df_bund_abs['schluessel'].isin(crimes))
        ][[
            'schluessel', # =crime_type
            'year',
            'sexus',
            'straftat', # =crime_type
        ]]
        # Add the crime_type (=age_group)
        df_overview_pie[age_group] = df_bund_abs[age_group]

        return df_overview_pie
    

    # --------------------------------------
    # Load Data
    # (all the needed data for the dashboard)
    # --------------------------------------
    
    # Load dataframes from Postgres database
    # Agreed Names of the needed dataframes are:
    # df_bund_abs -> absolute numbers for Germany
    # df_bund_rel -> relative numbers for 100.000 residents
    # df_laender_abs -> absolute numbers for the federal states of Germany
    # df_laender_rel-> relative numbers for 100.000 residents per state
    df_bund_abs = get_dataframe("SELECT * FROM public.bund_jugend_tat_absolut_2022_until_2018;")
    df_bund_rel = get_dataframe("SELECT * FROM public.bund_jugend_tat_relativ_2022_until_2018;")
    df_laender_abs = get_dataframe("SELECT * FROM public.laender_jugend_tat_absolut_2022_until_2018;")
    df_laender_rel = get_dataframe("SELECT * FROM public.laender_jugend_tat_relativ_2022_until_2018;")

    # Load Geo-Data needed for maps (containing federal states of Germany)
    @st.cache_data
    def get_geodata():
        with open('data/bundeslaender_polygons.json') as f:
            geo_data = json.load(f)
        return geo_data
    geo_data = get_geodata()
    

    # --------------------------------------
    # Session variables 
    # (for storing states of the dashboard)
    # --------------------------------------
    if 'year' not in st.session_state:
        st.session_state['year'] = 2022
    if 'federal_state' not in st.session_state:
        st.session_state['federal_state'] = 'Germany'
    if 'age_group' not in st.session_state:
        st.session_state['age_group'] = 'All'
    if 'crime_type' not in st.session_state:
        st.session_state['crime_type'] = 'All'
    if 'gender' not in st.session_state:
        st.session_state['gender'] = 'All'
    

    #------------------------
    # Other needed variables
    #------------------------
    federal_states = ['Germany', 'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen',
                      'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 
                      'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland', 'Sachsen',
                      'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen'
    ]
    
    # Keys of selected crimes (these keys are used in the data of BKA)
    crime_types = {'All':['------'],
                   'Homicide': ['010000', '020010'], #Tötungen
                   'Assault': ['220000'], #Körperverletzung
                   'Sexual Offence': ['100000'], #Sexuelle Straftaten
                   'Deprivation of Liberty': ['232100'], #Freiheitsberaubung
                   'Coercion': ['232200', '232201', '232279'], #Nötigung
                   'Burglary': ['435*00'], #Wohnungseinbruchdiebstahl
                   'Shoplifting': ['*26*00'], #Ladendiebstahl
                   'Robbery': ['21000'], #Raub
                   'Drug/Narcotics': ['730000', '891100'], #Drogen/Betäubungsmittel
                   'Damage to Property': ['674000'], #Sachbeschädigung
    }
    
    # Defined age groups
    age_groups = {"All": 'tatverdaechtige_insgesamt',
                  "14 to <16": 'jugendliche_14_bis_unter_16',
                  "16 to <18": 'jugendliche_16_bis_unter_18',
                  "18 to <21": 'heranwachsende_18_bis_unter_21',
                  "14 to <21": 'jugendl_u_heranwachsende_14_bis_unter_21',
    }

    # Define Gender groups
    genders = {
        'All': 'X',
        'Female': 'W',
        'Male': 'M'
    }


    # -------------------------------------------------------------------------
    # Sidebar
    # (The sidebar of the app with dashboard controls and further info's)
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.subheader('Dashboard Controls')
        st.slider(':calendar: Year', key='year', min_value=2018, max_value=2022, value=2022)
        st.selectbox(':flag-de: Federal State', federal_states, key='federal_state')
        st.selectbox(' Age Group', age_groups, key='age_group')
        st.selectbox(':mag: Type of Crime', crime_types, key='crime_type')
        st.radio(':yin_yang: Gender', genders, key='gender')
        st.button(':sunny: Reset', on_click=reset)

        st.markdown("<hr style='margin-top:0.5rem; margin-bottom:0.5rem; padding-top:0; padding-bottom:0;'>", unsafe_allow_html=True)
        
        st.markdown("#### :wave: Interested in us?  ")
        sidebar_col1, sidebar_col2= st.columns([1, 8])
        with sidebar_col1:
            st.image('img/linkedin_icon.png', width=20)
        with sidebar_col2:
            st.markdown("""Visit us  
                        [Johanna Köpke]()  
                        [Julie Laur](https://www.linkedin.com/in/julie-laur-a4167713a/)  
                        [Alexander Schuppe](https://www.linkedin.com/in/alexander-schuppe/)  
                        """)

        st.markdown("<hr style='margin-top:0.5rem; margin-bottom:0.1; padding-top:0; padding-bottom:0;'>", unsafe_allow_html=True)

        st.caption('Impressum')
    

    # -------------------
    # Show the Dashboard
    # -------------------
    tab_germany, tab_states, tab_cities = st.tabs(['Germany', 'States', 'Cities'])

    with tab_germany:
        st.markdown(f"<h3 style='margin-bottom:0rem; padding-bottom:0rem;'>Juvenile Crime in Germany {st.session_state['year']}</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-top:0.3rem; padding-top:0rem;'>Overview</h5>", unsafe_allow_html=True)

        tab_germany_col1, tab_germany_col2 = st.columns(2)

        with tab_germany_col1:

            df = get_df_overview_map(st.session_state['year'], crime_types[st.session_state['crime_type']], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
            fig1 = px.choropleth_mapbox(
                df,
                locations = 'bundesland',
                geojson = geo_data,
                featureidkey = 'properties.NAME_1',
                color = age_groups[st.session_state['age_group']],
                height=600,
                width=600,
                zoom = 4.8,
                opacity=0.3,
                title='Overall Crime Rates Distribution'
            )
            fig1.update_layout(mapbox_style='carto-positron')
            fig1.update_mapboxes(center={'lat':51.31, 'lon':10.5}) #Flinsberg, middle of Germany
            fig1.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig1)

        with tab_germany_col2:
            # Line-Chart with overview years
            df = get_df_overview_linechart(crime_types[st.session_state['crime_type']], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
            fig2 = px.line(
                x=df['year'], 
                y=df[age_groups[st.session_state['age_group']]], 
                markers=True,
                title = 'Absolute Crime Rate over Years'
            )
            fig2.update_xaxes(type='category') #set to categorical datatype so that on x-axis no in between values are calculated by plotly
            fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            fig2.update_layout(
                # title = straftat + ' - ' + age_group.replace('_', ' ').title(),
                xaxis_title = 'Year',
                yaxis_title = 'Number of Crimes'
            )
            st.plotly_chart(fig2)

            # Pie-Chart
            df = get_df_overview_pie(st.session_state['year'], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
            fig3 = px.pie(
                df, 
                values=age_groups[st.session_state['age_group']], 
                names='straftat', 
                title='Types of Crime',
            )
            st.plotly_chart(fig3)

    

    with tab_states:
        st.markdown(f"<h3 style='margin-bottom:0rem; padding-bottom:0rem;'>Juvenile Crime in Germany {st.session_state['year']}</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-top:0.3rem; padding-top:0rem;'>Federal States of Germany</h5>", unsafe_allow_html=True)
        st.write('Will come soon')
    


    with tab_cities:
        st.markdown(f"<h3 style='margin-bottom:0rem; padding-bottom:0rem;'>Juvenile Crime in Germany {st.session_state['year']}</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-top:0.3rem; padding-top:0rem;'>Federal States of Germany</h5>", unsafe_allow_html=True)
        st.write('Will come if enough time is left')
