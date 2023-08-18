# -----------------------------------------------------
# Juvenile Crime in Germany.
# Dashboard for the capstone project of Data Analyst Bootcamp (may to august 2023) of neuefische.
# 
# Created by: 
# Johanna Köpke.
# Julie Laur.
# Alexander Schuppe.
# -----------------------------------------------------


# Import the needed libraries
import json
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# from st_pages import Page, show_pages, hide_pages
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
                    padding-top: 0rem;
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

# Hide Multipage Buttons on top of sidebar
st.markdown("<style>.css-79elbk {display: none;}</style>", unsafe_allow_html=True)


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

# Show the input field for the password
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
        st.session_state['abs_rel'] = 'Relative'
    

    def get_df_map(crime, year, age_group, gender):
        '''
        Get the data for plotting the Map.
        @crime (list of str): The 'schluessel' = crime_type from the DB to be filtered.
        @year (int): The year to be filtered
        @age_group (str): One of the age_group's from the DB.
        @gender (str): Male (M), Female (F) or both (X).
        @return (pandas.Dataframe): The filtered Dataframe with the data needed to plot the map.
        '''
        df_map = df_laender_abs_rel[
            (df_laender_abs_rel['schluessel'].isin(crime)) &
            (df_laender_abs_rel['year'] == year) &
            (df_laender_abs_rel['age_group'] == age_group) &
            (df_laender_abs_rel['sexus'] == gender)
        ]
        return df_map
    

    def get_top_crimes_germany(year, age_group, gender):
        '''
        Create a table from global df_overview_state to make a bar chart
        with top crimes.
        @year (int): The year for which the top crimes shall be shown.
        @age_group (str): The age group the chart shall be shown for.
        @gender (str): The gender from the SQL table.
        @return (pandas.Dataframe): The Dataframe from which to plot the bar chart.
        '''
        df_top_crimes_germany = df_overview_state[
            (df_overview_state['year'] == year) &
            (df_overview_state['age_group'] == age_group) &
            (df_overview_state['sexus'] == gender)
        ][[
            'year',
            'schluessel_crimes_on_rank_1',
            'crimes_on_rank_1',
            'percentage_of_rank_1_on_crime_total',
            'schluessel_crimes_on_rank_2',
            'crimes_on_rank_2',
            'percentage_of_rank_2_on_crime_total',
            'schluessel_crimes_on_rank_3',
            'crimes_on_rank_3',
            'percentage_of_rank_3_on_crime_total',
            'schluessel_crimes_on_rank_4',
            'crimes_on_rank_4',
            'percentage_of_rank_4_on_crime_total',
            'schluessel_crimes_on_rank_5',
            'crimes_on_rank_5',
            'percentage_of_rank_5_on_crime_total'
        ]]
        # Build new dataframe becaue of twisted rows/columns (needed for bar chart)
        df_top_crimes_germany.reset_index(drop=True, inplace=True)
        data = []
        for row in range(0,9,3):
            # because of the twisted structure of the table jump always 3 columns
            tmp = []
            for col in range(1,4):
                if col in (2, 5, 8):
                    # the rows wich contain the crime name - have to be shortened
                    tmp.append(df_top_crimes_germany.iat[0, row+col].split(' ')[0])
                else:
                    # leave other rows as they are
                    tmp.append(df_top_crimes_germany.iat[0, row+col])
            data.append(tmp)
        df_data = pd.DataFrame(data)
        df_data.columns = ['schluessel', 'crime_type', 'percentage']
        # Try translation of crime types from german to english
        df_data['crime_type'] = df_data['crime_type'].apply(lambda x: crime_german_to_english[ df_data.query("crime_type==@x")[['schluessel']].iat[0,0] ])
        # return new dataframe
        return df_data
    

    def get_top_crimes_federal_states(state, year, age_group, gender):
        '''
        Create a table from global df_overview_fed_states to make a bar chart
        with top crimes.
        @state (str): The federal state for which the chart shall be created.
        @year (int): The year for which the top crimes shall be shown.
        @age_group (str): The age group the chart shall be created for.
        @gender (str): The gender from the SQL table to filter for.
        @return (pandas.Dataframe): The Dataframe from which to plot the bar chart.
        '''
        df_top_crimes_federal_states = df_overview_fed_states[
            (df_overview_fed_states['bundesland'] == state) &
            (df_overview_fed_states['year'] == year) &
            (df_overview_fed_states['age_group'] == age_group) &
            (df_overview_fed_states['sexus'] == gender)
        ][[
            'bundesland',
            'year',
            'schluessel_crimes_on_rank_1',
            'crimes_on_rank_1',
            'percentage_of_rank_1_on_crime_total',
            'schluessel_crimes_on_rank_2',
            'crimes_on_rank_2',
            'percentage_of_rank_2_on_crime_total',
            'schluessel_crimes_on_rank_3',
            'crimes_on_rank_3',
            'percentage_of_rank_3_on_crime_total',
            'schluessel_crimes_on_rank_4',
            'crimes_on_rank_4',
            'percentage_of_rank_4_on_crime_total',
            'schluessel_crimes_on_rank_5',
            'crimes_on_rank_5',
            'percentage_of_rank_5_on_crime_total'
        ]]
        # Build new dataframe becaue of twisted rows/columns (needed for bar chart)
        df_top_crimes_federal_states.set_index('bundesland', inplace=True)
        data = []
        for i in range(1,4):
            data.append([
                df_top_crimes_federal_states.at[state, f"schluessel_crimes_on_rank_{i}"],
                df_top_crimes_federal_states.at[state, f"crimes_on_rank_{i}"].split(' ')[0],
                df_top_crimes_federal_states.at[state, f"percentage_of_rank_{i}_on_crime_total"],
            ])
        df_data = pd.DataFrame(data)
        df_data.columns = ['schluessel', 'crime_type', 'percentage']
        # Try translation of crime types from german to english
        df_data['crime_type'] = df_data['crime_type'].apply(lambda x: crime_german_to_english[ df_data.query("crime_type==@x")[['schluessel']].iat[0,0] ])
        # return new dataframe
        return df_data
    

    def get_df_overview_pie(state, year, age_group, gender):
        '''
        Create a table from global table 'df_distribution_crime' for making a pie chart out of it.
        @state (str): The federal state (including Germany as a whole).
        @year (int): The year the pie chart should be filtered to.
        @age_group (string): The name of the column in the database for the filtered age group.
        @gender (string): The gender to filter for.
        @return (pandas.Dataframe): The dataframe to make a pie chart from.
        '''
        # Correct entry in dataframe if Germany as whole is selected
        if state == 'Germany':
            state = 'Bundesrepublik Deutschland'

        # Make a list of all crimes for the pie chart
        crimes = [crime for crime in crime_types.values()] #use the global variable
        crimes = sum(crimes, []) #flatten the list of lists of schluessel
        crimes.remove('------')
        crimes.append('other')

        # Filter the dataframe and return only what is needed
        df_overview_pie = df_distribution_crime[
            (df_distribution_crime['bundesland'] == state) &
            (df_distribution_crime['year'] == year) &
            (df_distribution_crime['age_group'] == age_group) &
            (df_distribution_crime['sexus'] == gender) &
            (df_distribution_crime['schluessel'].isin(crimes))
        ][[
            'bundesland',
            'year',
            'age_group',
            'sexus',
            'schluessel', # =crime_type
            'straftat', # =crime_type
            'certain_crime_percent_of_total_crime'
        ]]
        # Shorten the names of the crimes
        # df_overview_pie['straftat'] = df_overview_pie['straftat'].apply(lambda x: x.split(' ')[0])

        # Translate long german crime names to short english names

        df_overview_pie['straftat'] = df_overview_pie['schluessel'].apply(lambda x: crime_german_to_english[x])
        # return the dataframe
        return df_overview_pie
    

    def get_df_overview_linechart(state, crime_type, age_group, gender):
        '''
        Create a table from global table 'df_bund_laender_abs_rel' for making a linechart out of it.
        @state (str): The federal state to show.
        @crime_type (list of string): The 'schluessel' of different crime types.
        @age_group (string): The name of the column in the database for the filtered age group.
        @gender (string): The gender to filter for.
        @return (pandas.Dataframe): The dataframe to make a linechart from.
        '''
        if state == 'Germany':
            state = 'Bundesrepublik Deutschland' 
        df_overview_linechart = df_bund_laender_abs_rel[
            (df_bund_laender_abs_rel['bundesland'] == state) &
            (df_bund_laender_abs_rel['schluessel'].isin(crime_type)) &
            (df_bund_laender_abs_rel['age_group'] == age_group) &
            (df_bund_laender_abs_rel['sexus'] == gender)
        ]
        # Calculate the sum for the crime_type, if there are several 'schluessel'
        #df_overview_linechart = df_overview_linechart.groupby('year', as_index=False).sum()
        return df_overview_linechart
    

    def get_df_growth_rate(state, crime_type, year, age_group, gender):
        '''
        Create a table from global table 'df_growth_rate' for showing growth rates of crime.
        @state (str): The federal state (including Germany as a whole).
        @crime_type (list of string): The 'schluessel' of different crime types.
        @year (int): The year the pie chart should be filtered to.
        @age_group (string): The name of the column in the database for the filtered age group.
        @gender (string): The gender to filter for.
        @return (pandas.Dataframe): The dataframe to make a linechart from.
        '''
        if state == 'Germany':
            state = 'Bundesrepublik Deutschland'

        df_growth = df_growth_rate[
            (df_growth_rate['bundesland'] == state) &
            # (df_growth_rate['year'] == year) &
            (df_growth_rate['age_group'] == age_group) &
            (df_growth_rate['sexus'] == gender) &
            (df_growth_rate['schluessel'].isin(crime_type))
        ]
        return df_growth
    
    
    # --------------------------------------
    # Load Data
    # (all the needed data for the dashboard)
    # --------------------------------------
    
    # Load dataframes from Postgres database
    df_bund_abs = get_dataframe("SELECT * FROM public.bund_jugend_tat_absolut_2022_until_2018;")
    df_bund_rel = get_dataframe("SELECT * FROM public.bund_jugend_tat_relativ_2022_until_2018;")
    df_laender_abs = get_dataframe("SELECT * FROM public.laender_jugend_tat_absolut_2022_until_2018;")
    df_laender_rel = get_dataframe("SELECT * FROM public.laender_jugend_tat_relativ_2022_until_2018;")
    df_overview_fed_states = get_dataframe("SELECT * FROM public.df_overview_fed_states_2022_until_2018;")
    df_overview_state = get_dataframe("SELECT * FROM public.df_overview_state_2022_until_2018;")
    df_distribution_crime = get_dataframe("SELECT * FROM public.df_distribution_crime_2022_until_2018;")
    df_growth_rate = get_dataframe("SELECT * FROM public.df_growth_rate_2022_until_2018;")
    df_laender_abs_rel = get_dataframe("SELECT * FROM public.df_laender_abs_rel_2022_until_2018;")
    df_bund_laender_abs_rel = get_dataframe("SELECT * FROM public.df_bund_laender_abs_rel_2022_until_2018;")
    

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
    if 'abs_rel' not in st.session_state:
        st.session_state['abs_rel'] = 'Relative'
    

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
                #    'Other': ['other'],
                   'Homicide': ['010000, 020010'], #Mord und Totschlag
                   'Assault': ['220000'], #Körperverletzung
                   'Sexual offences': ['100000'], #Sexuelle Straftaten
                   'Deprivation of liberty': ['232100'], #Freiheitsberaubung
                   'Coercion': ['232200'], #Nötigung
                   'Residential burglary': ['435*00'], #Wohnungseinbruchdiebstahl
                   'Shoplifting': ['*26*00'], #Ladendiebstahl
                   'Robbery': ['210000'], #Raub
                   'Drug offences (w/o procurement)': ['730000'], #Rauschgiftdelikte (ohne Beschaffungskriminalität)
                   'Drug procurement crime': ['891100'], #Rauschgift-Beschaffungskriminalität
                   'Damage to property': ['674000'], #Sachbeschädigung
    }
    
    # Defined age groups
    age_groups = {"All": 'jugendl_u_heranwachsende_14_bis_unter_21',
                  "14 to <16": 'jugendliche_14_bis_unter_16',
                  "16 to <18": 'jugendliche_16_bis_unter_18',
                  "18 to <21": 'heranwachsende_18_bis_unter_21',
                #   "14 to <21": 'jugendl_u_heranwachsende_14_bis_unter_21',
    }

    # Define Gender groups
    genders = {
        'All': 'X',
        'Female': 'W',
        'Male': 'M'
    }

    # Translate keys of crimes to shortened english names
    crime_german_to_english = {
        '010000, 020010': 'Homicide',
        '220000': 'Assault',
        '100000': 'Sexual offences',
        '232100': 'Deprivation of liberty',
        '232200': 'Coercion',
        '435*00': 'Residential burglary',
        '*26*00': 'Shoplifting',
        '210000': 'Robbery',
        '730000': 'Drug offences (w/o procurement)',
        '891100': 'Drug procurement crime',
        '674000': 'Damage to property',
        'other': 'other'
    }

    # The Years for which the Dashboard has data
    years = [2018, 2019, 2020, 2021, 2022]

    # SVG images (arrows and circles) for growth rate
    arrow_down = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" fill="{color}" class="bi bi-arrow-down-right-circle" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8zm15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.854 5.146a.5.5 0 1 0-.708.708L9.243 9.95H6.475a.5.5 0 1 0 0 1h3.975a.5.5 0 0 0 .5-.5V6.475a.5.5 0 1 0-1 0v2.768L5.854 5.146z"/>
                    </svg>"""
    arrow_up = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" fill="{color}" class="bi bi-arrow-up-right-circle" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8zm15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.854 10.803a.5.5 0 1 1-.708-.707L9.243 6H6.475a.5.5 0 1 1 0-1h3.975a.5.5 0 0 1 .5.5v3.975a.5.5 0 1 1-1 0V6.707l-4.096 4.096z"/>
                    </svg>"""
    circle = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" fill="{color}" class="bi bi-dash-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                    <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                </svg>"""


    # -------------------------------------------------------------------------
    # Sidebar
    # (The sidebar of the app with dashboard controls and further info's)
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("<h3 style='margin-top:1rem;'>Dashboard Controls</h3>", unsafe_allow_html = True)
        st.slider(':calendar: Year', key='year', min_value=min(years), max_value=max(years))
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

        impressum_de = st.button("Impressum")
        if impressum_de:
            switch_page("impressum_de")
    

    # -------------------
    # Show the Dashboard
    # -------------------


    # --------------------------------------
    # Corretions for displaying in Dashboard
    # --------------------------------------

    # Correct the Display of Gender
    sex = ''
    if st.session_state['gender'] == 'Male':
        sex = 'M'
    elif st.session_state['gender'] == 'Female':
        sex = 'F'
    else:
        sex = 'X'
    
    # Correct the Display of age
    age = ''
    if st.session_state['age_group'] == '14 to <16':
        age = '14 to under 16'
    elif st.session_state['age_group'] == '16 to <18':
        age = '16 to under 18'
    elif st.session_state['age_group'] == '18 to <21':
        age = '18 to under 21'
    elif st.session_state['age_group'] == 'All':
        #age_group 'All'
        age = '14 to under 21'
    

    # st.markdown(f"<h3 style='margin-top:-0.5rem; padding-top:0; margin-bottom:1rem; padding-bottom:0rem;'>Juvenile Crime in Germany {st.session_state['year']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-top:-0.5rem; padding-top:0; margin-bottom:1rem; padding-bottom:0rem;'>Juvenile Crime in Germany</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.5, 0.5])

    with col1:

        # ----------------------------
        # Map on the left side
        # ----------------------------
        # Get the data
        df1 = get_df_map(crime_types[st.session_state['crime_type']], st.session_state['year'], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
        
        # Choose relative/absolute values
        if st.session_state['abs_rel'] == 'Relative':
            color_column = 'offenders_rel'
        else:
            color_column = 'offenders'
       
        # Create the map
        fig1 = px.choropleth_mapbox(
            df1,
            locations = 'bundesland', #column in dataframe
            geojson = geo_data, #geodata in geoJSON format
            featureidkey = 'properties.NAME_1', #key that merges to dataframe
            hover_name = 'bundesland',
            color = color_column,
            hover_data = {'schluessel': False,
                          'straftat': True,
                          'bundesland': False, 
                          'year': False, 
                          'age_group': False,
                          'sexus': False,
                          'offenders': True,
                          'offenders_rel': True, 
            }, 
            labels = {
                    'straftat': 'Crime',
                    # 'year': 'Year',
                    'offenders': 'Offenders absolute',
                    'offenders_rel': 'Offenders per 100,000 residents',
            },
            zoom=4.8,
            height=550,
            # width=600,
            opacity=0.4,
        )
        fig1.update_layout(
            mapbox_style='carto-positron',
            margin=dict(l=0, t=0, r=0, b=0),
            coloraxis_colorbar_title_text = '', #setzt einen Titel über der colorleiste am Rand
        )
        fig1.update_mapboxes(center=dict(lat=51.4, lon=10.5)) #Flinsberg, middle of Germany
        fig1.update_coloraxes(showscale=True)
        # Show in Dashboard
        
        #sex -> {genders[st.session_state['gender']]}
        #age -> {age_groups[st.session_state['age_group']]}
        st.markdown(f"<h6 style='margin-bottom:0rem; padding-bottom:0rem;'>Offenders {st.session_state['abs_rel']}</h6>", unsafe_allow_html=True)
        st.markdown(f"""<div style='margin-bottom:0.5rem; padding-bottom:0rem; font-size: 0.9em;'>
                            <b>Crime:</b> {st.session_state['crime_type']}<br>
                            <b>Age:</b> {age} &nbsp;&nbsp;&nbsp;
                            <b>Gender:</b> {sex} &nbsp;&nbsp;&nbsp;
                            <b>Year:</b> {st.session_state['year']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
        st.plotly_chart(fig1, use_container_width=True)
        # Show the dataframe
        # st.dataframe(df1, use_container_width = True)

        # Radio Buttons to choose between absolute/relative values
        st.radio('Choose what values to show in the map', options=['Relative', 'Absolute'], key='abs_rel', horizontal=True)


    with col2:

        # ----------------------------
        # Rank - Top 3 Crimes (Bar Chart)
        # ----------------------------
        if st.session_state['federal_state'] == 'Germany':
            # Get data
            df2 = get_top_crimes_germany(st.session_state['year'], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
            # Create bar chart
            fig2 = px.bar(df2, 
                          x='crime_type', 
                          y='percentage',
                          height = 360,
                          text = 'percentage', #show values in chart
                          labels = {
                            'crime_type': 'Crime',
                            'percentage': 'Percentage'
                          },
                          hover_name = 'crime_type',
                          hover_data = {
                              'crime_type': False,
                              'percentage': True
                          }
            )
            fig2.update_xaxes(tickangle=-45)
            fig2.update_xaxes(type='category')
            fig2.update_layout(
                xaxis_title = '',
                yaxis_title = 'Percentage',
            )
            # Show it in Dashboard
            st.markdown(f"<h6 style='margin-bottom:0rem; padding-bottom:0rem;'>Top 3 Crimes in {st.session_state['federal_state']}</h6>", unsafe_allow_html=True)
            st.markdown(f"""<div style='margin-bottom:0rem; padding-bottom:0rem; font-size: 0.9em;'>
                            <b>Age:</b> {age} &nbsp;&nbsp;&nbsp;
                            <b>Gender:</b> {sex} &nbsp;&nbsp;&nbsp;
                            <b>Year:</b> {st.session_state['year']}
                        </div>""", 
                        unsafe_allow_html=True
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Show the table
            # st.dataframe(df2, use_container_width = True, hide_index = True)
        else:
            # Get data
            df2 = get_top_crimes_federal_states(st.session_state['federal_state'], st.session_state['year'], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
            # Create bar chart
            fig2 = px.bar(df2, 
                          x='crime_type', 
                          y='percentage',
                          height = 360,
                          text = 'percentage', #show values in chart
                          labels = {
                            'crime_type': 'Crime',
                            'percentage': 'Percentage'
                          },
                          hover_name = 'crime_type',
                          hover_data = {
                              'crime_type': False,
                              'percentage': True
                          }
            )
            fig2.update_xaxes(tickangle=-45)
            fig2.update_xaxes(type='category')
            fig2.update_layout(
                xaxis_title = '',
                yaxis_title = 'Percentage',
            )
            # Show it in Dashboard
            st.markdown(f"<h6 style='margin-bottom:0rem; padding-bottom:0rem;'>Top 3 Crimes in {st.session_state['federal_state']}</h6>", unsafe_allow_html=True)
            st.markdown(f"""<div style='margin-bottom:0rem; padding-bottom:0rem; font-size: 0.9em;'>
                            <b>Age:</b> {age} &nbsp;&nbsp;&nbsp;
                            <b>Gender:</b> {sex} &nbsp;&nbsp;&nbsp;
                            <b>Year:</b> {st.session_state['year']}
                        </div>""", 
                        unsafe_allow_html=True
            )
            st.plotly_chart(fig2, use_container_width=True)
            # Show the table
            # st.dataframe(df2, use_container_width = True, hide_index = True)


        # ----------------------------
        # Crime Types (Pie Chart)
        # ----------------------------
        # Get data
        df3 = get_df_overview_pie(st.session_state['federal_state'], st.session_state['year'], age_groups[st.session_state['age_group']], genders[st.session_state['gender']])
        # Create Chart
        fig3 = px.pie(
            df3, 
            values='certain_crime_percent_of_total_crime', 
            names='straftat', 
            height = 450,

        )
        # fig3.update_layout(
        #     showlegend=True,
        #     margin=dict(l=0, t=10, r=0, b=0),
        #     legend=dict(
        #         yanchor="bottom",
        #         y=-0.8,
        #         xanchor="left",
        #         x=0
        #     ),
        # )
        fig3.update_traces(
            textposition = 'inside',
            # textinfo = 'label+value'
            textinfo = 'label+percent'
        )
        # Show it on Dashboard
        st.markdown(f"<h6 style='margin-bottom:0rem; padding-bottom:0rem;'>Types of Crime</h6>", unsafe_allow_html=True)
        st.markdown(f"""<div style='margin-bottom:0; padding-bottom:0; font-size: 0.9em;'>
                        <b>State:</b> {st.session_state['federal_state']} &nbsp;&nbsp;&nbsp;
                    </div>""", 
                    unsafe_allow_html=True
        )
        st.markdown(f"""<div style='padding-top:0; margin-bottom:0; padding-bottom:0; font-size: 0.9em;'>
                        <b>Age:</b> {age}, &nbsp;&nbsp;&nbsp;
                        <b>Gender:</b> {sex} &nbsp;&nbsp;&nbsp;
                        <b>Year:</b> {st.session_state['year']}
                    </div>""", 
                    unsafe_allow_html=True
        )
        st.plotly_chart(fig3, use_container_width=True)
        # Show the table
        # st.dataframe(df3)
    

    st.markdown(f"<h4 style='margin-top:0; padding-top:0; margin-bottom:1.5rem; padding-bottom:0rem;'>Overview of Years</h4>", unsafe_allow_html=True)

    # ----------------------------
    # Growth Rate (Just Numbers)
    # ----------------------------
    # Get values for all years
    df6 = get_df_growth_rate(st.session_state['federal_state'], 
                             crime_types[st.session_state['crime_type']], 
                             st.session_state['year'], 
                             age_groups[st.session_state['age_group']], 
                             genders[st.session_state['gender']])
    
    # Get absolute and relative values for each year
    abso = {}
    rela = {}
    for y in years:
        tmp = df6[df6['year'] == y]
        tmp.reset_index(drop=True, inplace=True)
        abso[y] = tmp.iat[0, 6]
        rela[y] = tmp.iat[0, 7]
    # Add an arrow - if value is positiv -> arrow_up, if value is negativ -> arrow_down, else -> cirle
    red = '#ec5347'
    green = '#5abf41'
    blue = '#1a60bc'
    gray = '#eef0f4'
    dgray = '#757989'
    size = 20
    # Add arrow to absolute values
    for key, val in abso.items():
        if abso[key] == 'n.a.':
            abso[key] = [abso[key], circle.format(size=size, color=dgray)]
        elif float(abso[key]) < 0:
            abso[key] = [abso[key], arrow_down.format(size=size, color=green)]
        elif float(abso[key]) > 0:
            abso[key] = [abso[key], arrow_up.format(size=size, color=red)]
    # Add arrow to relative values
    for key, val in rela.items():
        if rela[key] == 'n.a.':
            rela[key] = [rela[key], circle.format(size=size, color=dgray)]
        elif float(rela[key]) < 0:
            rela[key] = [rela[key], arrow_down.format(size=size, color=green)]
        elif float(rela[key]) > 0:
            rela[key] = [rela[key], arrow_up.format(size=size, color=red)]
    
    # Show it on Dashboard
    
    col5, col6 = st.columns(2)    
    
    # Define CSS for the card to show the numbers
    st.markdown("""
                <style>.box{
                    padding: 3px;
                    margin: 2px;
                    border:1px solid;
                    border-radius: 10px;
                    display: inline-block;
                    text-align: center;
                }</style>
                """, 
                unsafe_allow_html=True)
    
    with col5:          
        
        st.markdown(f"""
                    <div style='border:1px solid; border-color: #e3e7ee; padding: 15px; border-radius: 10px;'>
                        <h5 style='margin-bottom:0.5rem; padding-bottom:0rem;'>{arrow_up.format(size=32, color=blue)}&nbsp;&nbsp;Growth Rates in %</h5>
                        <h6 style='margin-top:0rem; margin-bottom:0.5rem; padding-bottom:0rem;'>Absolute</h6>
                        <span style='margin-bottom: 0.7rem; display:block;'>
                        <b>State:</b> {st.session_state['federal_state']},
                        <b>Year:</b> {st.session_state['year']},
                        <b>Crime:</b> {st.session_state['crime_type']}<br>
                        <b>Age:</b> {age},
                        <b>Gender:</b> {sex}<br>
                        </span>
                        <span class=box><span style='font-size:0.8rem;'>2018</span><br><span style='font-size:1.1rem;'>{abso[2018][0]}</span><br>{abso[2018][1]}</span>
                        <span class=box><span style='font-size:0.8rem;'>2019</span><br><span style='font-size:1.1rem;'>{abso[2019][0]}</span><br>{abso[2019][1]}</span>
                        <span class=box><span style='font-size:0.8rem;'>2020</span><br><span style='font-size:1.1rem;'>{abso[2020][0]}</span><br>{abso[2020][1]}</span>
                        <span class=box><span style='font-size:0.8rem;'>2021</span><br><span style='font-size:1.1rem;'>{abso[2021][0]}</span><br>{abso[2021][1]}</span>
                        <span class=box><span style='font-size:0.8rem;'>2022</span><br><span style='font-size:1.1rem;'>{abso[2022][0]}</span><br>{abso[2022][1]}</span>
                    </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
                    <div style='border:1px solid; border-color: #e3e7ee; padding: 15px; border-radius: 10px;'>
                    <h5 style='margin-bottom:0.5rem; padding-bottom:0rem;'>{arrow_up.format(size=32, color=blue)}&nbsp;&nbsp;Growth Rates in %</h5>
                    <h6 style='margin-top:0rem; margin-bottom:0.5rem; padding-bottom:0rem;'>Relative</h6>
                    <span style='margin-bottom: 0.7rem; display:block;'>
                    <b>State:</b> {st.session_state['federal_state']},
                    <b>Year:</b> {st.session_state['year']},
                    <b>Crime:</b> {st.session_state['crime_type']}<br>
                    <b>Age:</b> {age},
                    <b>Gender:</b> {sex}<br>
                    </span>
                    <span class=box><span style='font-size:0.8rem;'>2018</span><br><span style='font-size:1.1rem;'>{rela[2018][0]}</span><br>{rela[2018][1]}</span>
                    <span class=box><span style='font-size:0.8rem;'>2019</span><br><span style='font-size:1.1rem;'>{rela[2019][0]}</span><br>{rela[2019][1]}</span>
                    <span class=box><span style='font-size:0.8rem;'>2020</span><br><span style='font-size:1.1rem;'>{rela[2020][0]}</span><br>{rela[2020][1]}</span>
                    <span class=box><span style='font-size:0.8rem;'>2021</span><br><span style='font-size:1.1rem;'>{rela[2021][0]}</span><br>{rela[2021][1]}</span>
                    <span class=box><span style='font-size:0.8rem;'>2022</span><br><span style='font-size:1.1rem;'>{rela[2022][0]}</span><br>{rela[2022][1]}</span>
                    </div>
        """, unsafe_allow_html=True)
        
    # Show the table
    # st.dataframe(df6)


    col3, col4 = st.columns(2)

    with col3:
        # ----------------------------
        # Overview Years Absolute (Line Chart)
        # ----------------------------
        df4 = get_df_overview_linechart(st.session_state['federal_state'], 
                                        crime_types[st.session_state['crime_type']], 
                                        age_groups[st.session_state['age_group']], 
                                        genders[st.session_state['gender']]
        )
        fig4 = px.line(
            x=df4['year'], 
            y=df4['offenders'], 
            markers=True,
        )
        fig4.update_xaxes(type='category') #set to categorical datatype so that on x-axis no in between values are calculated by plotly
        fig4.update_layout(margin = dict(l=0, t=25, r=0, b=0), height=250)
        fig4.update_layout(
            xaxis_title = 'Year',
            yaxis_title = 'No. Offenders'
        )
        fig4.update_traces(line_color="#1a60bc")
        # Show on Dashboard        
        st.plotly_chart(fig4, use_container_width=True)
        # Show the table
        # st.dataframe(df4)
    

    with col4:
        # ----------------------------
        # Overview Years Relative (Line Chart)
        # ----------------------------
        df5 = get_df_overview_linechart(st.session_state['federal_state'], 
                                        crime_types[st.session_state['crime_type']], 
                                        age_groups[st.session_state['age_group']], 
                                        genders[st.session_state['gender']]
        )
        fig5 = px.line(
            x=df5['year'], 
            y=df5['offenders_rel'], 
            markers=True,
        )
        fig5.update_xaxes(type='category') #set to categorical datatype so that on x-axis no in between values are calculated by plotly
        fig5.update_layout(margin = dict(l=0, t=25, r=0, b=0), height=250)
        fig5.update_layout(
            xaxis_title = 'Year',
            yaxis_title = 'No. Offenders / 100.000'
        )
        fig5.update_traces(line_color="#1a60bc")
        # Show on Dashboard        
        st.plotly_chart(fig5, use_container_width=True)
        # Show the table
        # st.dataframe(df5)

# Give it some space at the bottom for scrolling down a little bit further    
st.write('')
st.write('')
st.write('')

# ---
# And this is the end.
# ---
# At the end everything is good.
# And if it is not good,
# it is not the end.
# ---