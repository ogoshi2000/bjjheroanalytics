from flask import request, render_template
from flask.blueprints import Blueprint
from app.models import Match, Fighter, db
from app.apis.fighters.bjj_fighters import get_fighter_id_by_name


bjj_matches = Blueprint("bjj_matches", __name__, template_folder="templates")


@bjj_matches.route("/", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        matches = Match.query.all()
        return [match.to_dict() for match in matches]
    if request.method == "POST":
        data = request.get_json()
        if isinstance(data, list):
            matches = []
            for match_data in data:
                match = Match(
                    fighter_id=get_fighter_id_by_name(match_data["name"]),
                    opponent=match_data["opponent"],
                    opponent_id=get_fighter_id_by_name(match_data["opponent"]),
                    w_l=match_data["w_l"],
                    method=match_data["method"],
                    competition=match_data["competition"],
                    stage=match_data["stage"],
                    weight=match_data["weight"],
                    year=match_data["year"],
                )
                matches.append(match)
            db.session.add_all(matches)
            db.session.commit()
            return [match.to_dict() for match in matches]
        else:
            match = Match(
                fighter_id=get_fighter_id_by_name(match_data["name"]),
                opponent=match_data["opponent"],
                opponent_id=get_fighter_id_by_name(match_data["opponent"]),
                w_l=match_data["w_l"],
                method=match_data["method"],
                competition=match_data["competition"],
                stage=match_data["stage"],
                weight=match_data["weight"],
                year=match_data["year"],
            )
            db.session.add(match)
            db.session.commit()
            return match.to_dict()


@bjj_matches.route("/methods", methods=["GET"])
def get_methods():
    methods = Match.query.with_entities(Match.method).distinct().all()
    return [method[0] for method in methods]


@bjj_matches.route("/network", methods=["GET"])
def get_network():
    matches = Match.query.filter(Match.opponent_id.isnot(None)).all()
    fighters = Fighter.query.all()
    nodes = [{"id": fighter.id, "label": fighter.name} for fighter in fighters]
    edges = list(frozenset((match.fighter.id, match.opponent_id) for match in matches))
    edges = [{"from": edge[0], "to": edge[1]} for edge in edges]
    
    return render_template("network.jinja2", nodes=nodes, edges=edges)
