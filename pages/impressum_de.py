import streamlit as st
from streamlit_extras.switch_page_button import switch_page


# ---------------------------------
# Layout/Styling
# (Some configurations for Streamlit)
# ---------------------------------
st.set_page_config(
    page_title = 'Juvenile Crime in Germany', 
    page_icon = ':bar_chart:', 
    layout = "wide", # or 'centered'
    initial_sidebar_state = "collapsed", #"auto"
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




# ---------------------
# Show on page
# ---------------------
col1, col2, col3 = st.columns([0.3, 0.6, 0.1])

with col2:
    st.markdown(f"<h3 style='margin-top:-0.5rem; padding-top:0; margin-bottom:1rem; padding-bottom:0rem;'>Juvenile Crime in Germany</h3>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='margin-top:0; padding-top:0; margin-bottom:0; padding-bottom:0rem;'>Impressum</h5>", unsafe_allow_html=True)

    st.markdown(f"<h6 style='margin-top:2rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Allgemeines</h6>", unsafe_allow_html=True)
    st.markdown("""
                Dieses Dashboard ist Teil des Abschlussprojektes des [neue fische](https://www.neuefische.de/) _Advanced Data Analyst Bootcamp_ (Mai bis August 2023).  
                Unser Team besteht aus:  
                - [Johanna Köpke]()  
                - [Julie Laur](https://www.linkedin.com/in/julie-laur-a4167713a/)  
                - [Alexander Schuppe](https://www.linkedin.com/in/alexander-schuppe/)  

                Wenn sie Interesse an unserer Arbeit haben, kontaktieren sie uns gerne.  
                """)

    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Quellenangaben</h6>", unsafe_allow_html=True)
    st.markdown("""Für dieses Projekt haben wir die folgenden Datenquellen verwendet:  
                - [PKS Bundeskriminalamt, 2018 - 2022](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/pks_node.html)  
                - [Statistisches Bundesamt DESTATIS](https://www.destatis.de/DE/Home/_inhalt.html)  
                """)
    
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Responsible</h6>", unsafe_allow_html=True)

    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Haftungsausschluss</h6>", unsafe_allow_html=True)
    st.markdown("""
                Dieses Projekt ist weder mit dem Bundeskriminalamt (BKA) noch mit demStatistischen Bundesamt (Destatis) verbunden, 
                aber es werden deren offizielle, frei zugängliche Daten verwendet.  
                Es werden keine Garantien für die Richtigkeit der hier dargestellten Daten übernommen.  
                """)

    st.markdown("")
    back = st.button("Zurück zum Dashboard")
    if back:
        switch_page("app")