# Juvenile Crime in Germany
## Distribution and Frequency Development  
<br>

### To Alexandra and Sergio  
---
Please review the <a href='https://github.com/alexmahesh/Crime_GER/blob/main/app.py' target='_blank'>app.py</a> file.  
You can find the running Dashboard here: <a href='https://crime-germany.streamlit.app/' target='_blank'>Juvenile Crime in Germany</a> (password as communicated).  
<br>
### Next ToDo  
---
- implement the possibility to choose between absolute and relative numbers  
- implement Federal States Tab 
- <br>
### Overview  
---
This is the Dashboard for our capstone project in the Data Analyst Bootcamp of neuefische (may to august 2023).  
We are:  
- <a href='#'>Johanna Köpke</a>  
- <a href='https://www.linkedin.com/in/julie-laur-a4167713a/' target='_blank'>Julie Laur</a>  
- <a href='https://www.linkedin.com/in/alexander-schuppe/' target='_blank'>Alexander Schuppe</a>  

The Dashboard shows different statistics and gives insights about juvenile crime in Germany.  
<br>
### The Data  
---
The Data used for this Dashboard comes from:  
- <a href='https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/pks_node.html' target='_blank'>German Federal Criminal Police Office: PKS Bundeskriminalamt, 2018 - 2022, Version 2.0</a>  
- <a href='https://www.destatis.de/DE/Home/_inhalt.html' target='_blank'>German Federal Statistical Office: Statistisches Bundesamt (Destatis), 2023</a>  
  <br>
### Technical Overview  
---
__Dashboard__  
The Dashboard is coded completely in Python with <a href='https://streamlit.io/' target='_blank'>Streamlit</a>. It is hosted with a free account  on the Streamlit-Server.  

__Database__  
It loads the needed data from several tables stored in a PostgreSQL-Database hosted on <a href='https://azure.microsoft.com/de-de/' target='_blank'>Microsoft Azure</a>.  

__Charts__  
The Charts are created with <a href='https://plotly.com/' target='_blank'>Plotly</a>.  
<br>
### Usage  
---
### __Sidebar__  
<img src='img/side_controls.png' height='300' />  
The Dashboard has several controls that are located in the sidebar on the left. The sidebar can be opened or hidden.  

### __Tabs__  
<img src='img/tabs.png' height='70'/>  
The Dashboard currently has 3 Tabs to show different information:  
- Germany : Showing overview information about juvenile crime rates in whole Germany.  
- States : Showing more specialized information about the juvenile crime rates in the federal states of Germany.  
- Cities : Showing specialized information about juvenile crime rates in the top 7 cities (concerning number of residents) of Germany.  

### __Germany-Tab__  
---
On this tab you can change:  
- Year (choosing between 2018 to 2022),  
- Crime Type (choosing between selected crime types that are relevant for Juveniles),  
- Age Group (choosing between defined age groups that are relevant for german laws),  
- Gender (differentiating between female and male).  
<br>

__Map on Germany-Tab__  
Showing crime distribution over whole Germany.  
<img src='img/map.png' height='200'/>  
<br>

__Linechart on Germany-Tab__  
Showing absolute crime rate over years.  
<img src='img/linechart.png' height='200'/>  
<br>

__Piechart on Germany-Tab__  
Showing distribution of selected types of crime that are relevant for Juveniles.  
<img src='img/piechart.png' height='180'/>  
<br>

### __States-Tab__  
---
Will be implemented next.  
On this tab you can change/find:  
- The same controls as on the Germany tab  
- Federal States (choosing out of the 16 federal states of Germany to see more detailed Information)  
- Information about the top 3 ranked crimes per state  
<br>

### __Cities-Tab__  
---
Will be implemented if there is time left in the project.  
Will show detail information about the 7 top cities of Germany (concerning number of inhabitants). 