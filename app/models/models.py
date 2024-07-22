from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Fighter(db.Model):
    __tablename__ = "fighter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return f"Fighter: {self.name}"


class Match(db.Model):
    __tablename__ = "match"
    id = db.Column(db.Integer, primary_key=True)
    fighter_id = db.Column(db.Integer, db.ForeignKey("fighter.id"), nullable=False)
    opponent = db.Column(db.String(200), nullable=False)  # Name of the opponent
    opponent_id = db.Column(db.Integer, db.ForeignKey("fighter.id"), nullable=True)
    w_l = db.Column(db.String(30), nullable=False)
    method = db.Column(db.String(100), nullable=False)
    competition = db.Column(db.String(100), nullable=False)
    stage = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=False)

    fighter = db.relationship(
        "Fighter", foreign_keys=[fighter_id], backref=db.backref("matches", lazy=True)
    )
    
    opponent_fighter = db.relationship(
        "Fighter",
        foreign_keys=[opponent_id],
        uselist=False,
        backref=db.backref("opponent_matches", lazy=True),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fighter_id": self.fighter_id,
            "opponent": self.opponent,
            "opponent_id": self.opponent_id,
            "w_l": self.w_l,
            "method": self.method,
            "competition": self.competition,
            "stage": self.stage,
            "weight": self.weight,
            "year": self.year,
        }

    def __repr__(self):
        if self.opponent_id:
            return f"<Match {self.id}: Fighter ID {self.fighter_id} vs. Opponent ID {self.opponent_id}>"
        else:
            return (
                f"<Match {self.id}: Fighter ID {self.fighter_id} vs. {self.opponent}>"
            )
