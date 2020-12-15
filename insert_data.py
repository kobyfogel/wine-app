import json

from wine import db
from wine.models import Wine
from sqlalchemy.exc import IntegrityError

with open('wine.json', encoding="utf-8") as json_file: 
    data = json.load(json_file) 


data = data['7000'] 
for line in data:
    new_wine = Wine(**line)
    try:
        db.session.add(new_wine)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
