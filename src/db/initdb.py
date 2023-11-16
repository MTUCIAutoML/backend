from db.session import engine
import models

def initdb():
    models.base.Seba.metadata.create_all(engine)


