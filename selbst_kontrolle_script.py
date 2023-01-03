# -*- coding: utf-8 -*-
# !/usr/bin/python
from datetime import datetime, timedelta
import pandas as pd
import joblib
import random
import os

class Progress:
    def __init__(self):
        self.all_possible_question = {}
        self.starttime = datetime.now()
        self.endtime = datetime.now()
        self.succesfull = []
        self.answercounter = 0

if __name__ == '__main__':
    all_possible_question = {}
    laws_question = {}

    # First open and read the files
    laws = pd.read_excel('./gesetze_recht.xlsx')
    laws = laws.fillna('')
    questions_abwl = pd.read_excel('./fragen_abwl.xlsx')
    questions_recht = pd.read_excel('./fragen_recht.xlsx')

    # Construct all possible questions
    for index, row in questions_abwl.iterrows():
        all_possible_question[len(all_possible_question)] = {'section': 'ABWL Fragen',
                                                             'question': row['Frage'],
                                                             'answer': row['Antwort']}
    for index, row in questions_recht.iterrows():
        all_possible_question[len(all_possible_question)] = {'section': 'RECHT Fragen',
                                                             'question': row['Frage'],
                                                             'answer': row['Antwort']}

    for index, row in laws.iterrows():
        if len(str(row['Für Dumme'])) > 0:
            laws_question[len(laws_question)] = {'section': 'RECHT Gesetze',
                                                 'question': f"In welchem Gesetz wird das folgende beschrieben: \"{row['Für Dumme']}\" ?",
                                                 'answer': f"{row['Artikel']}. {row['Titel']}\n\n{row['Inhalt']}"}
        if len(str(row['Inhalt'])) > 0:
            laws_question[len(laws_question)] = {'section': 'RECHT Gesetze',
                                                 'question': f"Wie lautet der Artikel in dem dieses Gesetz nieder geschrieben ist: \"{row['Inhalt']}\" ?",
                                                 'answer': f"{row['Artikel']}. {row['Titel']}"}

        if len(str(row['Beispiel 1'])) > 0 and len(str(row['Referenzantwort 1'])) > 0:
            laws_question[len(laws_question)] = {'section': 'RECHT Gesetze',
                                                 'question': row['Beispiel 1'],
                                                 'answer': row['Referenzantwort 1']}

        if len(str(row['Beispiel 1'])) > 0 and len(str(row['Referenzantwort 1'])) < 0:
            laws_question[len(laws_question)] = {'section': 'RECHT Gesetze',
                                                 'question': f"Nenne ein Beispiel für dieses Gesetz {row['Artikel']}. {row['Titel']}",
                                                 'answer': row['Beispiel 1']}

        if len(str(row['Für Dumme'])) > 0:
            laws_question[len(laws_question)] = {'section': 'RECHT Gesetze',
                                                 'question': f"Erkläre das Gesetz {row['Artikel']}. {row['Titel']}. Was steht hier drinnen?",
                                                 'answer': row['Für Dumme']}

        if len(str(row['Verweißende Gesetze'])) > 0:
            laws_question[len(laws_question)] = {'section': 'RECHT Gesetze',
                                                 'question': f"Wenn du ein Fall bearbeitest, in dem das Gesetzt \"{row['Artikel']}. {row['Titel']}\" zu Grunde liegt, welche Gesetze lohnt es sich nochmal anzuschauen?",
                                                 'answer': row['Verweißende Gesetze']}

    # StartUp of Program:
    progress = None
    try:
        progress = joblib.load('./progress.pkl')
        temp_diff = (progress.endtime - progress.starttime)
        progress.starttime = datetime.now() - temp_diff
        progress.endtime = datetime.now()
        i = input(f'Möchtest du deinen letzten Fortschritt laden? JA (j)')
        if i != 'j':
            raise Exception
    except Exception as e:
        progress = Progress()
        i = input(f'Möchtest du auch die Gesetze lernen? JA (j)')
        if i == 'j':
            for key, value in laws_question.items():
                all_possible_question[len(all_possible_question)] = value
        progress.all_possible_question = all_possible_question

    while len(progress.succesfull) != len(progress.all_possible_question):
        #try:
            os.system('cls')
            timediff = (len(progress.all_possible_question) - len(progress.succesfull)) * ((datetime.now() - progress.starttime) / len(progress.succesfull))
            timediff = str(timediff).split(".")[0]
            print(f'Statusbericht:\t\t'
                  f'\nAnzahl an gegeben Antworten: {progress.answercounter}\t\t So viele Fragen gibt es aktuell: {len(progress.all_possible_question)}'
                  f'\nSo viel kannst du schon: {round(100/len(progress.all_possible_question)*len(progress.succesfull), 2)}%'
                  f'\nZeit bis du wahrscheinlich alles kannst: {timediff}'
                  f'\n-----------------------------------------------------')


            question_number = random.randint(0, len(progress.all_possible_question))
            while question_number in progress.succesfull:
                question_number = random.randint(0, len(progress.all_possible_question))

            print(f"{progress.all_possible_question[question_number]['section']}\n")
            print(f"\033[94m{progress.all_possible_question[question_number]['question']}\033[0m")
            input(f'\n -> Antwort anzeigen (Enter drücken)')
            print(f"\n\033[94m{progress.all_possible_question[question_number]['answer']}\033[0m")
            i = input(f'\n -> Korrekt geantwortet ? JA (j)')
            if i == 'j':
                progress.succesfull.append(question_number)

            progress.answercounter += 1
            progress.endtime = datetime.now()
            joblib.dump(progress, './progress.pkl')
        #except Exception as e:
        #    print(f'Error: {e}')

    input('DU HAST ALLE FRAGEN GESCHAFFT !')