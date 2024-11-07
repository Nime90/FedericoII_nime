#import relevant libraries
import pandas as pd
import requests
from utils import finding_variables
from bs4 import BeautifulSoup
link_profilcultura = 'https://www.profilcultura.it/annuncio/Lavoro-Beni-Culturali-Politiche-Culturali-Turismo'
Full_tab = pd.DataFrame()
Pages = [1,2,3,4,5,6,7,8]
#finding all links:
for p in Pages:
    try:
        Job_lists = requests.get(link_profilcultura+'-page'+str(p))

        soup = BeautifulSoup(Job_lists.text, 'html.parser')

        #finding Links
        All_jobs = soup.find_all('a')
        links = []
        to_avoid = ['/Lavoro', '/contratto/', '/regione/', '/category/','/ajout','/professione/']
        for l in All_jobs:
            href = str(l.get('href'))
            if not any(item in href for item in to_avoid) and '/annuncio/' in str(l.get('href')):
                links.append(l.get('href'))

        #finding job name
        Names = []
        All_names=soup.find_all('aside')
        for n in All_names:
            try:Names.append(n.h4.contents[0])
            except:pass

        for idx, url in enumerate(links):
            content = requests.get(url)

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(content.text, 'html.parser')

            # Find specific elements, for example all links
            All_info=soup.find_all('aside')

            #finding Variables
            output_variables, output_columns = finding_variables(All_info)

            #initiate a Table:
            Table = pd.DataFrame()
            Table['Job_title'] = [str(Names[idx])]
            Table['url'] = [str(url)]
            #adding the other columns
            for i,c in enumerate (output_columns):
                Table[c] = output_variables[i]

            #Storing data into the general database
            Full_tab = pd.concat([Full_tab,Table])
    except:
        break
Full_tab.reset_index(inplace=True, drop = True)

Full_tab.to_excel('dataset_Full_results.xlsx', index = False)