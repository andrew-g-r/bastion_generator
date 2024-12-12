import random
import json
import pprint

#load json
with open ('bastion_free.json', encoding='utf8') as f:
    data = json.load(f)

#return dice list of dice rolls from string <n>d<n> '3d6' rolls and dice faces
def roll(dice_string):
    rolls, dice = map(int, dice_string.split('d'))
    return [
        random.randint(1, dice)
        for _ in range(rolls)
    ]

#create dictionary of id strings    
def closest(k, lst=[1,11,21,31,41,51,61,71,81,91]):
    return str(lst[min(range(len(lst)), key = lambda i: abs(lst[i]-k))])

#consult the table of failed careers based on lowest and highest of 3d6 stats    
def make_job():
    job_stats = stats()
    if max(job_stats) >= 12:
        job = (max(job_stats)%10*10)+2+min(min(job_stats),12)
    elif max(job_stats) == 11:
        job = 13+min(job_stats)
    elif max(job_stats) == 10:
        job = min(job_stats)+5
    else:
        job = min(job_stats)-2
    job = closest(job)
    return job, job_stats, roll('1d6'), roll('1d6'), roll('1d6'), roll('1d6')

#create a table of 3 stats
def stats():
    stats = []
    for i in range(3):
        stats.append(sum(roll('3d6')))
    return stats

#find career by id in json
def json_seek(id_):
    for p in data['career']:
        if p['id'] == id_:
            return p

#create the failed career objects
class fail:
    kind = 'Failed Career'
    def __init__(self, name):
        self.name = name
        self.stats = make_job()
        self.job = self.stats[0]
        self.job_data = json_seek(self.job)
        self.job_title = self.job_data['title']
        self.job_desc = self.job_data['desc']
        self.job_get = self.job_data['get']
        self.job_debt1 = self.job_data['debt1']
        self.job_debt2 = self.job_data['debt2']
        self.job_prompt1 = self.job_data['tables']['prompt1']
        self.job_answer1 = self.job_data['tables']['table1'][str(self.stats[4][0])]
        self.job_prompt2 = self.job_data['tables']['prompt2']
        self.job_answer2 = self.job_data['tables']['table2'][str(self.stats[5][0])]
        self.details()
    def notes(self, notes):
        self.notes = notes
    def details(self):
        job = self.stats
        self.data = {
        "career": self.job_title,
        "desc": self.job_desc,
        "stats": job[1],
        "hp": job[2],
        "pocket money":job[3],
        "get": self.job_get,
        "debt1": self.job_debt1,
        "debt2": self.job_debt2,
        "prompt1": self.job_prompt1,
        "answer1": self.job_answer1,
        "prompt2": self.job_prompt2,
        "answer2": self.job_answer2,
        }
        pprint.pp(self.data, sort_dicts=False)