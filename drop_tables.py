from wine import db


db.drop_all()
db.create_all()
db.commit()