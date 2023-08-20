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

# Hide arrow of sidebar
st.markdown("<style>.eyeqlp51 {display: none;}</style>", unsafe_allow_html=True)



# ---------------------
# Show on page
# ---------------------
german = st.button('🇩🇪')
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

with col2:
    st.markdown(f"<h3 style='margin-top:-0.5rem; padding-top:0; margin-bottom:1rem; padding-bottom:0rem;'>Juvenile Crime in Germany</h3>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='margin-top:0; padding-top:0; margin-bottom:0; padding-bottom:0rem;'>Legal Notice</h5>", unsafe_allow_html=True)

    # Commons
    st.markdown(f"<h6 style='margin-top:2rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Commons</h6>", unsafe_allow_html=True)
    st.markdown("""
                This dashboard is part of the final project of the [neue fische](https://www.neuefische.de/) _Advanced Data Analyst Bootcamp_ (May bis August 2023).  
                Our team consists of:  
                - [Johanna Köpke]()  
                - [Julie Laur](https://www.linkedin.com/in/julie-laur-a4167713a/)  
                - [Alexander Schuppe](https://www.linkedin.com/in/alexander-schuppe/)  

                If you are interested in our work, please contact us.  
                """)

    # References
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>References</h6>", unsafe_allow_html=True)
    st.markdown("""
                For this project, we used the following data sources:     
                - [PKS Bundeskriminalamt, 2018 - 2022, Version 2.0](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/pks_node.html)   
                - [Statistisches Bundesamt DESTATIS](https://www.destatis.de/DE/Home/_inhalt.html)   
                """)
    # Scope
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Scope</h6>", unsafe_allow_html=True)
    st.markdown("""
                The numbers of offenders were analyzed for the following offences.  
                The relative numbers of offenders were calculated on the basis of the population figures in the respective age groups. The population figures of 31 December of the respective previous year (reporting date) were used.    
                """)
    st.markdown("""| BKA Schluessel | Crime German | Crime English |  
| -------------- | -------------------------------------------------------- | ------------------------------- |  
| ------ | Straftaten insgesamt | Total offences |  
| 100000 | Straftaten gegen die sexuelle Selbstbestimmung insgesamt | Sexual offences |  
| 210000 | Raub, räuberische Erpressung und räuberischer Angriff auf Kraftfahrer §§ 249-252, 255, 316a StGB | Robbery |  
| 220000 | Körperverletzung §§ 223-227, 229, 231 StGB | Assault |  
| 232100 | Freiheitsberaubung § 239 StGB | Deprivation of liberty |  
| 232200 | Nötigung § 240 StGB | Coercion |  
| 435*00 | Wohnungseinbruchdiebstahl §§ 244 Abs. 1 Nr. 3 und Abs. 4, 244a StGB | Residential burglary |  
| *26*00 | Ladendiebstahl insgesamt | Shoplifting |  
| 674000 | Sachbeschädigung §§ 303-305a StGB | Damage to property |  
| 730000 | Rauschgiftdelikte (soweit nicht bereits mit anderer Schlüsselzahl erfasst) | Drug offences (w/o procurement) |  
| 891100 | direkte Beschaffungskriminalität | Drug procurement crime |  
| 010000, 020010 | Mord § 211 StGB, Totschlag § 212 StGB | Homicide |  
""")
    
    # Legal Notice
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Legal Notice</h6>", unsafe_allow_html=True)
    st.markdown("""
                Responsible for the content:  
                Johanna Köpke  
                Ernst-Horn-Str. 18b  
                22525 Hamburg   
                Email:  johanna.kpk@googlemail.com  

                Julie Laur  
                Schanzenstr. 33a  
                20357 Hamburg   
                Email:  julie.laur648@gmx.de  

                Alexander Schuppe  
                Eimsbütteler Chaussee 85  
                20259 Hamburg  
                Email: mail@alexanderschuppe.de  
                """)
    
    # Privacy policy
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Privacy policy</h6>", unsafe_allow_html=True)
    st.markdown("""
                This dashboard does not store any personal data and does not use cookies.    
                The site uses the free hosting offer of [Streamlit](https://streamlit.io/). You can find more information on their data protection details at: [Streamlit Privacy Policy](https://streamlit.io/privacy-policy)  
                """, unsafe_allow_html=True)

    # Technology
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Technology</h6>", unsafe_allow_html=True)
    st.markdown("""
                The following techniques were used to create the dashboard:  
                - Python, Pandas, Numpy, Jupyter Notebook  
                - SQL, PostgreSQL, Azure, DBeaver  
                - GitHub/Git  
                - MS Excel, Google Docs Editors  
                - VSCode  

                """)
    
    # Disclaimer
    st.markdown(f"<h6 style='margin-top:3rem; padding-top:0; margin-bottom:0.3rem; padding-bottom:0rem;'>Disclaimer</h6>", unsafe_allow_html=True)
    st.markdown("""
                This project is not affiliated with the Bundeskriminalamt (BKA) or the Statistischen Bundesamt (Destatis), 
                but their official, freely accessible data are used.  
                No guarantees are made for the accuracy of the data and correlations presented here.  
                """)

    st.write('')
    st.write('')
    back = st.button("Back to Dashboard")
    st.write('')
    st.write('')

    if back:
        switch_page("app")
    elif german:
        switch_page('impressum_de')