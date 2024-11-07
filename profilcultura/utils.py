def finding_variables(All_info):
    Data_pubblicazione = None
    Contratto = None
    Posizione = None
    Azienda_Istituzione = None
    Sito_Azienda_Istituzione = None
    Settore = None
    Descrizione_Azienda_Istituzione = None
    Descrizione_posizione_lavorativa = None
    Profilo = None
    Esperienza = None
    Data_inizio = None
    Candidatura_entro = None
    Retribuzione = None
    Luogo_di_lavoro = None
    URL_Bando = None
    
    for t in All_info:
        if 'left_offre' in str(t):
            Posizione = t.h4.contents[0]
            Azienda_Istituzione = t.p.contents[0]

        elif 'right_offre' in str(t):
            Data_pubblicazione = str(str(t).split('<p>')[1].replace('<span class="date">','')).split('</span>')[0]
            Contratto = str(t).split('<p>')[2].replace('</p>\n','')

        elif 'Sito web'  in str(t):
            Sito_Azienda_Istituzione = t.a.get('href')

        elif 'Settore' in str(t):
            Settore = str(t.contents[2]).strip()
        
        elif 'Azienda/Istituzione'  in str(t):
            Descrizione_Azienda_Istituzione = str(t.contents[2]).strip()
        
        elif 'Posizione lavorativa' in str(t):
            Descrizione_posizione_lavorativa = str(t).split('</h3>')[1].replace('</aside>', '').strip()
        
        elif 'Profilo ricercato' in str(t):
            Profilo = str(t).split('</h3>')[1].replace('</aside>', '').strip()

        elif 'Candidatura entro'  in str(t):
            Candidatura_entro = str(t).split('</h3>')[1].replace('</aside>', '').strip()

        elif 'Retribuzione' in str(t):
            Retribuzione = str(t).split('</h3>')[1].replace('</aside>', '').strip()

        elif 'Luogo di lavoro' in str(t):
            Luogo_di_lavoro = str(t).split('</h3>')[1].replace('</aside>', '').strip()
        
        ###Following NEEEDS TO BE DOUBLE CHECKED
        elif 'Esperienza richiesta' in str(t): 
            Esperienza = str(t).split('</h3>')[1].replace('</aside>', '').strip()

        elif 'Inizio previsto' in str(t):
            Data_inizio = str(t).split('</h3>')[1].replace('</aside>', '').strip()

        elif 'URL bando/avviso' in str(t):
            URL_Bando = str(t).split('</h3>')[1].replace('</aside>', '').strip()
    
    output_variables = [Data_pubblicazione, Contratto, Posizione ,Azienda_Istituzione,Sito_Azienda_Istituzione,
                    Settore, Descrizione_Azienda_Istituzione, Descrizione_posizione_lavorativa,
                    Profilo, Esperienza, Data_inizio, 
                    Candidatura_entro, Retribuzione, Luogo_di_lavoro, URL_Bando]
    
    output_columns = ['Data pubblicazione','Contratto','Posizione','Azienda/Istituzione','Sito Azienda/Istituzione',
                    'Settore','Descrizione Azienda/Istituzione','Descrizione posizione lavorativa',
                    'Descrizione profilo ricercato','Descrizione esperienza richiesta','Data di inizio prevista',
                    'Data limite candidature','Retribuzione','Luogo_di_lavoro','URL bando/avviso']
    
    return output_variables, output_columns