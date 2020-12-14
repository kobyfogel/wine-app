import csv

from wine import db


with open('7000.csv', encoding="utf-8") as f:
    data=[tuple(line) for line in csv.reader(f)]


query = "INSERT INTO wine ('country', 'description', 'points', 'province', 'title', 'variety', 'winery', 'user_id') VALUES"
for line in data[1:]:
    new_line = (line[1:-1]) + ("NULL",)
    db.session.execute(f"{query} {line};")
db.session.commit()