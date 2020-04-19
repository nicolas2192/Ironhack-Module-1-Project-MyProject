# IronHack Bootcamp Module 1 Project

### :boom: Core technical concepts and inspiration
This was the first project of the Ironhack Data Analytics Bootcamp. The main goal was to gather meaningful insights from a data set about the wealthiest men and women on earth. All steps taken to access and enhance the data as well as the main python modules used to perform such actions are described as follows:

- Access the database (sqlalchemy and SQL queries)

- Data manipulation and cleaning (Pandas, Requests, BeautifulSoup)

- Reporting (Matplotlib, Email)

### :computer: Process description
What this analysis tries to confirm is whether there is a relevant difference between men and women. The main hurdle I encountered while performing the analysis was that both, nationality and gender column, had a significant amount of null and empty fields.
This was handled by accessing a free API which returned a gender (Male or Female) by providing a name. This method gave good results, however, it was improved by providing a nationality alongside the name. Nationality, citizenship or birthplace was retrieved by parsing each millionaire's wikipedia page. The clearest example where nationality would be the name "Andrea", which is female in Spain but a men's name in Italy. 

<p align="center">
  <img width="540" height="480" src="readme/readme1.png">
</p>

### :bar_chart: Results
The analysis confirms what was previously thought, men outnumber women in all analyzed sectors. However, the distribution don't follow the same pattern in both genders. As can be seen in the bar chart, technology, finance and fashion will be the sectors where men's wealth is mostly allocated while fashion, food and manufactering where you could find the bulk of women's wealth. 

<p align="center">
  <img width="400" height="400" src="data/results/Gender_PieChart.png">
</p>

<p align="center">
  <img width="800" height="600" src="data/results/SectorGenderBarChart.png">
</p>

<img align="left" width="400" height="400" src="data/results/Gender_PieChart.png"><img align="right" width="500" height="300" src="data/results/SectorGenderBarChart.png">
