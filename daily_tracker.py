#!/home/arklez/codes/Git/daily-tracker/venv/bin/python
import csv
from datetime import date
import sys
import yaml

PREFIX = "/home/arklez/codes/Git/daily-tracker/"

CSV_PATH = PREFIX + "myresults.csv"
QUESTIONS_PATH = PREFIX + "myconfig.yml"
data = []

today = str(date.today())

with open(CSV_PATH) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        data.append(row)

if len(data) and data[-1]['timestamp'] == today:
    sys.exit()

# Load questions
questions = None
with open(QUESTIONS_PATH, 'r') as f:
    questions = yaml.safe_load(f)

def check_int_format(ans, lb = None, rb = None):
    try:
        x = int(ans)
        if lb is not None and lb > x:
            return False
        if rb is not None and rb < x:
            return False
    except:
        return False
    return True


def check_float_format(ans, lb = None, rb = None):
    try:
        x = float(ans)
        if lb is not None and lb > x:
            return False
        if rb is not None and rb < x:
            return False
    except:
        return False
    return True

def ask_likert(question: str) -> int:
    ans = input(f"{question} (likert): ")
    while not check_int_format(ans, 1, 7):
        print(f"This is not correct format for type likert")
        ans = input("Please, try again: ")
    return ans


def ask_int(question: str) -> int:
    ans = input(f"{question} (int): ")
    while not check_int_format(ans):
        print(f"This is not correct format for type int")
        ans = input("Please, try again: ")
    return ans

def ask_float(question: str) -> int:
    ans = input(f"{question} (float): ")
    while not check_float_format(ans):
        print(f"This is not correct format for type float")
        ans = input("Please, try again: ")
    return ans


def ask_prc(question: str) -> int:
    ans = input(f"{question} (percents): ")
    while not check_int_format(ans, 0, 100):
        print(f"This is not correct format for percents")
        ans = input("Please, try again: ")
    return ans

# Ask quetions
this_day = {'timestamp':today}
for qst_pair in questions:
    ans = None
    if qst_pair["type"] == 'likert':
        ans = ask_likert(qst_pair["question"])
    if qst_pair["type"] == 'int':
        ans = ask_int(qst_pair["question"])
    if qst_pair["type"] == 'prc':
        ans = ask_prc(qst_pair["question"])
    if qst_pair["type"] == 'float':
        ans = ask_float(qst_pair["question"])
    this_day[qst_pair["question"]] = ans

with open(CSV_PATH, 'w') as csvfile:
    fields = set(this_day.keys())
    if len(data):
        fields = fields.union(set(data[0].keys()))
    fields = list(fields)
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for day in data:
        writer.writerow(day)
    writer.writerow(this_day)

