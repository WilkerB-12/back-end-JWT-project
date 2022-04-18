from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    @classmethod
    def create(cls, **data):
        #crear instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print('FALLA EL CONSTRUCTOR')
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD: ',error.args)
            db.session.rollback()
            return None
            raise Exception(error.args, 500)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }