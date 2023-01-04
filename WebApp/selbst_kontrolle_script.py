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
        self.laws_question = {}


class Quiz:

    def load_questions(self):
        self.all_possible_question = {}
        self.laws_question = {}
        # First open and read the files
        laws = pd.read_excel('./gesetze_recht.xlsx')
        laws = laws.fillna('')
        questions_abwl = pd.read_excel('./fragen_abwl.xlsx')
        questions_recht = pd.read_excel('./fragen_recht.xlsx')

        # Construct all possible questions
        for index, row in questions_abwl.iterrows():
            self.all_possible_question[len(self.all_possible_question)] = {'section': 'ABWL Fragen',
                                                                'question': row['Frage'],
                                                                'answer': row['Antwort']}
        for index, row in questions_recht.iterrows():
            self.all_possible_question[len(self.all_possible_question)] = {'section': 'RECHT Fragen',
                                                                'question': row['Frage'],
                                                                'answer': row['Antwort']}

        for index, row in laws.iterrows():
            if len(str(row['Für Dumme'])) > 0:
                self.laws_question[len(self.laws_question)] = {'section': 'RECHT Gesetze',
                                                    'question': f"In welchem Gesetz wird das folgende beschrieben: \"{row['Für Dumme']}\" ?",
                                                    'answer': f"{row['Artikel']}. {row['Titel']}\n\n{row['Inhalt']}"}
            if len(str(row['Inhalt'])) > 0:
                self.laws_question[len(self.laws_question)] = {'section': 'RECHT Gesetze',
                                                    'question': f"Wie lautet der Artikel in dem dieses Gesetz nieder geschrieben ist: \"{row['Inhalt']}\" ?",
                                                    'answer': f"{row['Artikel']}. {row['Titel']}"}

            if len(str(row['Beispiel 1'])) > 0 and len(str(row['Referenzantwort 1'])) > 0:
                self.laws_question[len(self.laws_question)] = {'section': 'RECHT Gesetze',
                                                    'question': row['Beispiel 1'],
                                                    'answer': row['Referenzantwort 1']}

            if len(str(row['Beispiel 1'])) > 0 and len(str(row['Referenzantwort 1'])) < 0:
                self.laws_question[len(self.laws_question)] = {'section': 'RECHT Gesetze',
                                                    'question': f"Nenne ein Beispiel für dieses Gesetz {row['Artikel']}. {row['Titel']}",
                                                    'answer': row['Beispiel 1']}

            if len(str(row['Für Dumme'])) > 0:
                self.laws_question[len(self.laws_question)] = {'section': 'RECHT Gesetze',
                                                    'question': f"Erkläre das Gesetz {row['Artikel']}. {row['Titel']}. Was steht hier drinnen?",
                                                    'answer': row['Für Dumme']}

            if len(str(row['Verweißende Gesetze'])) > 0:
                self.laws_question[len(self.laws_question)] = {'section': 'RECHT Gesetze',
                                                    'question': f"Wenn du ein Fall bearbeitest, in dem das Gesetzt \"{row['Artikel']}. {row['Titel']}\" zu Grunde liegt, welche Gesetze lohnt es sich nochmal anzuschauen?",
                                                    'answer': row['Verweißende Gesetze']}

        for key, value in self.laws_question.items():
            self.all_possible_question[len(self.all_possible_question)] = value

    def get_question(self, username):
        # StartUp of Program:
        progress = None
        try:
            progress = joblib.load(f'./progress/progress{username}.pkl')
            temp_diff = (progress.endtime - progress.starttime)
            progress.starttime = datetime.now() - temp_diff
            progress.endtime = datetime.now()
            # i = input(f'Möchtest du deinen letzten Fortschritt laden? JA (j)')
            # if i != 'j':
            #     raise Exception
        except Exception as e:
            progress = Progress()
            # i = input(f'Möchtest du auch die Gesetze lernen? JA (j)')
            # i = 'j'
            # if i == 'j':
            #     for key, value in self.laws_question.items():
            #         self.all_possible_question[len(self.all_possible_question)] = value

        # while len(progress.succesfull) != len(progress.all_possible_question):
            # os.system('cls')
        timediff = (len(self.all_possible_question) - len(progress.succesfull)) * (datetime.now() - progress.starttime)
        timediff = str(timediff).split(".")[0]
        # returnstring = (f'Statusbericht:\t\t'
        #         f'\nAnzahl an gegeben Antworten: {progress.answercounter}\t\t So viele Fragen gibt es aktuell: {len(self.all_possible_question)}'
        #         f'\nSo viel kannst du schon: {round(100/len(self.all_possible_question)*len(progress.succesfull), 2)}%'
        #         f'\nZeit bis du wahrscheinlich alles kannst: {timediff}'
        #         f'\n-----------------------------------------------------')


        question_number = random.randint(0, len(self.all_possible_question))
        while question_number in progress.succesfull:
            question_number = random.randint(0, len(self.all_possible_question))

        # returnstring += f"{self.all_possible_question[question_number]['section']}\n"
        # returnstring += f"\033[94m{self.all_possible_question[question_number]['question']}\033[0m"
        # returnstring +=(f'\n -> Antwort anzeigen (Enter drücken)')
        # antwort = (f"\n\033[94m{self.all_possible_question[question_number]['answer']}\033[0m")
        # i = input(f'\n -> Korrekt geantwortet ? JA (j)')
        # if i == 'j':

        daten = DataObj()
        daten.answercounter = progress.answercounter
        daten.num_all_possible_question = len(self.all_possible_question)
        daten.num_succesfull = round(100/len(self.all_possible_question)*len(progress.succesfull), 2)
        daten.timediff = timediff
        daten.q_section = self.all_possible_question[question_number]['section'].replace("\n"," ")
        daten.q_question = self.all_possible_question[question_number]['question'].replace("\n"," ")
        daten.q_answer = self.all_possible_question[question_number]['answer'].replace("\n"," ")
        daten.q_number = question_number

        return daten

    def antwort(self, question_number, korrekt, username):
        progress = None
        try:
            progress = joblib.load(f'./progress/progress{username}.pkl')
        except Exception as e:
            progress = Progress()

        if korrekt == "1":
            progress.succesfull.append(question_number)

        progress.answercounter += 1
        progress.endtime = datetime.now()
        joblib.dump(progress, f'./progress/progress{username}.pkl')

        # return len(progress.succesfull) != len(progress.all_possible_question)

    # input('DU HAST ALLE FRAGEN GESCHAFFT !')

class DataObj:
    def __init__(self):
        self.answercounter = 0
        self.num_all_possible_question = 0
        self.num_succesfull = 0
        self.timediff = 0
        self.q_section = ""
        self.q_question = ""
        self.q_answer = ""
        self.q_number = 0