
# Import the needed libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy



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


# --- Here starts the Dashboard ---
#     Only visible after log-in
if st.session_state['logged_in']:
    
    @st.cache_data
    def get_dataframe(query):
        con = sqlalchemy.create_engine('postgresql://user:pass@host/database', connect_args=st.secrets.azure_db)
        df = pd.read_sql_query(sql=query, con=con)
        return df
    
    df_grund_bund = get_dataframe("select * from public.bund_grund_2022_until_2018 limit 10;")
    df_grund_bund

