from flask import request, render_template
from flask.blueprints import Blueprint
from app.models import Match, db
from app.apis.fighters.bjj_fighters import get_fighter_id_by_name
from sqlalchemy.orm import joinedload


bjj_matches = Blueprint("bjj_matches", __name__, template_folder="templates")


@bjj_matches.route("/", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        try:
            matches = Match.query.all()
            return [match.to_dict() for match in matches]
        except Exception as e:
            return str(e), 500
    if request.method == "POST":
        try:
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
        except Exception as e:
            return str(e), 500


@bjj_matches.route("/methods", methods=["GET"])
def get_methods():
    try:
        methods = Match.query.with_entities(Match.method).distinct().order_by(Match.method).all()
        return [method[0] for method in methods]
    except Exception as e:
        return str(e), 500

@bjj_matches.route("/competitions", methods=["GET"])
def get_competitions():
    try:
        competitions = Match.query.with_entitites(Match.competitiuon).distinct().order_by(Match.competition).all()
        return [competition[0] for competition in competitions]
    except Exception as e:
        return str(e), 500


# @bjj_matches.route("/network", methods=["GET"])
# def get_network():
#     match_query = Match.query
#     try:
#         for k, v in request.args.items():
#             if k in ["year", "method", "competition", "weight"]:
#                 match_query = match_query.filter(getattr(Match, k) == v)

#         matches = (
#             match_query.filter(Match.opponent_id.isnot(None))
#             .options(joinedload(Match.fighter))
#             .all()
#         )
#         fighters = list(
#             frozenset((match.fighter.id, match.fighter.name) for match in matches)
#         )
#         nodes = [{"id": fighter[0], "label": fighter[1]} for fighter in fighters]
#         edges = list(
#             frozenset((match.fighter.id, match.opponent_id) for match in matches)
#         )
#         edges = [{"from": edge[0], "to": edge[1]} for edge in edges]

#         return render_template("network.jinja2", nodes=nodes, edges=edges)
#     except Exception as e:
#         return str(e), 500

@bjj_matches.route("/network", methods=["GET"])
def get_netowrk_2():
    try:
        edges = db.session.query(Match.fighter.name,Match.opponent_fighter.name).select_from(Match).distinct().all()
        print(edges)
        return "hi"
    except Exception as e:
        return str(e), 500