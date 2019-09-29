class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
    cardid = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    telephone = db.Column(db.String(80))

	def __init__(self, cardid, name, email, telephone):
		self.cardid = cardid
		self.name = name
		self.email = email
		self.telephone = telephone
