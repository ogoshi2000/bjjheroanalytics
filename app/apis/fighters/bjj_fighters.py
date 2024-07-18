from flask import request
from flask.blueprints import Blueprint
from app.models import Fighter, Match, db
import json

bjj_fighters = Blueprint("bjj_fighters", __name__,template_folder="templates")


@bjj_fighters.route("/<int:id>", methods=["GET"])
def fighter_by_id(id):
    if request.method == "GET":
        fighter = Fighter.query.get(id)
        return fighter.to_dict()


@bjj_fighters.route("/", methods=["GET", "POST"])
def fighter():
    if request.method == "GET":
        fighters = Fighter.query.all()
        return [fighter.to_dict() for fighter in fighters]

    if request.method == "POST":
        data = json.loads(request.get_json())
        if isinstance(data, list):
            fighters = [Fighter(name=fighter_data) for fighter_data in data]
            db.session.add_all(fighters)
            db.session.commit()
            return [fighter.to_dict() for fighter in fighters]
        else:
            fighter = Fighter(name=data["Name"])
            db.session.add(fighter)
            db.session.commit()
            return fighter.to_dict()


@bjj_fighters.route("/search", methods=["GET"])
def get_fighter_id():
    if request.method == "GET":
        name = request.args.get("name")
        return {"name": name, "id": get_fighter_id_by_name(name)}


@bjj_fighters.route("/untracked", methods=["GET"])
def get_untracked_fighters():
    matches = (
        Match.query.filter_by(opponent_id=None)
        .distinct(Match.opponent)
        .with_entities(Match.opponent)
        .all()
    )
    return [match[0] for match in matches]


def get_fighter_id_by_name(name):
    fighter_id = Fighter.query.filter_by(name=name).with_entities(Fighter.id).first()
    return fighter_id[0] if fighter_id else None
