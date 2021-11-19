import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

column_names = ['Names', 'Phones', 'Website', 'Street', 'City', 'State', 'Zip', 'Clg_type', 'Award', 'Campus_setting',
                'Campus_housing', 'Student_population', 'Student_to_faculty_ratio']
df = pd.DataFrame(columns=column_names)
names, phones, website, address, street, city, state, zip_c, clg_type, award, campus_setting, campus_housing, student_population, student_to_faculty_ratio, institute_id = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
list_name = [names, phones, website, street, city, state, zip_c, clg_type, award, campus_setting, campus_housing,
             student_population, student_to_faculty_ratio]
for page in range(1, 35):
    URL = "https://nces.ed.gov/COLLEGENAVIGATOR/?s=all&l=91&pg=" + str(page)
    html_text = requests.get(URL).text
    soup = BeautifulSoup(html_text, "lxml")

    data = soup.find_all('p', class_='ipeds hoverID')

    for i in data:
        web_pattern = r'<p class="ipeds hoverID">IPEDS ID:(.*?) | OPE ID: 04283300  </p>'
        if re.search(web_pattern, str(i)) is not None:
            web = re.search(web_pattern, str(i)).group(1)
        else:
            web = 495217
        institute_id.append(web)

    data = soup.find_all('table', class_='itables')

    for i in data:
        names.append(i.find('h2').get_text())
        phones.append(i.find('td', class_='sra').get_text())
        address.append(re.search(r'</h2>(.*?)</td></tr><tr><td class="srb"', str(i)).group(1))
        clg_type_pattern = r'</td></tr><tr><td class="srb" scope="row">Type:  </td><td class="sra">(.*?)</td>'
        clg_type.append(re.search(clg_type_pattern, str(i)).group(1).replace('&lt; ', ''))
        award_pattern = r'Awards offered:  </td><td class="sra">(.*?)</td>'
        award.append(re.search(award_pattern, str(i)).group(1))
        campus_setting_pattern = r'Campus setting:  </td><td class="sra">(.*?)</td>'
        campus_setting.append(re.search(campus_setting_pattern, str(i)).group(1))
        campus_housing_pattern = r'Campus housing:  </td><td class="sra">(.*?)</td>'
        campus_housing.append(re.search(campus_housing_pattern, str(i)).group(1))
        student_population_pattern = r'Student population:  </td><td class="sra">(.*?)</td>'
        if re.search(student_population_pattern, str(i)) is not None:
            stud_count = re.search(student_population_pattern, str(i)).group(1)
        else:
            stud_count = 0
        student_population.append(stud_count)
        student_to_faculty_ratio_pattern = r'Student-to-faculty ratio:  </td><td class="sra">(.*?)</td>'
        if re.search(student_to_faculty_ratio_pattern, str(i)) is not None:
            stud_fact_ratio = re.search(student_to_faculty_ratio_pattern, str(i)).group(1)
        else:
            stud_fact_ratio = 0
        student_to_faculty_ratio.append(stud_fact_ratio)

for i in address:
    code = i.split()[-1]
    street.append(i.split(',')[0])
    city.append(i.split(',')[1])
    states = i.split(',')[-1].split()[:-1]
    if len(states) > 1:
        ans = ''
        for j in states:
            ans += j
            ans += " "
        ans = ans.strip()
        state.append(ans)
    else:
        state.append(states[0])
    zip_c.append(code)

for ii in institute_id:
    URL1 = URL + "&id=" + str(ii)

    html_text = requests.get(URL1).text
    soup2 = BeautifulSoup(html_text, "lxml")
    data = soup2.find_all('table', class_='layouttab')
    web_pattern_2 = r'target="_blank">(.*?)</a>'
    website.append(re.search(web_pattern_2, str(data)).group(1).strip())

for i, y in zip(column_names, list_name):
    df[i] = y
df.to_csv('final.csv')
