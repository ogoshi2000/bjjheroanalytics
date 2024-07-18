from flask import request
from flask.blueprints import Blueprint
from app.models import Fighter, Match, db
import json

bjj_fighters = Blueprint("bjj_fighters", __name__, template_folder="templates")


@bjj_fighters.route("/<int:id>", methods=["GET"])
def fighter_by_id(id):
    try:
        if request.method == "GET":
            fighter = Fighter.query.get(id)
            return fighter.to_dict()
    except Exception as e:
        return str(e), 500


@bjj_fighters.route("/", methods=["GET", "POST"])
def fighter():
    try:
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
    except Exception as e:
        return str(e), 500


@bjj_fighters.route("/search", methods=["GET"])
def get_fighter_id():
    try:
        if request.method == "GET":
            name = request.args.get("name")
            return {"name": name, "id": get_fighter_id_by_name(name)}
    except Exception as e:
        return str(e), 500


@bjj_fighters.route("/untracked", methods=["GET"])
def get_untracked_fighters():
    try:
        untracked_fighters = (
            Match.query.filter_by(opponent_id=None)
            .distinct(Match.opponent)
            .with_entities(Match.opponent)
            .all()
        )
        return [untracked_fighter[0] for untracked_fighter in untracked_fighters]
    except Exception as e:
        return str(e), 500


def get_fighter_id_by_name(name):
    try:
        fighter_id = Fighter.query.filter_by(name=name).with_entities(Fighter.id).first()
        return fighter_id[0] if fighter_id else None
    except Exception as e:
        return str(e), 500
