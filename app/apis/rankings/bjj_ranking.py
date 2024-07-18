from flask.blueprints import Blueprint
from app.models import Match, Fighter

bjj_ranking = Blueprint("bjj_ranking", __name__,template_folder="templates")


@bjj_ranking.route("/score-by-wins", methods=["GET"])
def get_score():
    fighter_scores = []
    fighters = Fighter.query.join(Match, Fighter.id == Match.fighter_id).all()
    for fighter in fighters:
        matches = fighter.matches
        points = 0
        for match in matches:
            if match.w_l == "W":
                points += 1
            if match.w_l == "L":
                points -= 1
        fighter_scores.append({"fighter": fighter.name, "score": points})
    return sorted(fighter_scores, key=lambda x: x["score"], reverse=True)


@bjj_ranking.route("/score-by-method", methods=["GET"])
def get_score_by_method():
    fighter_scores = []
    fighters = Fighter.query.join(Match, Fighter.id == Match.fighter_id).all()
    for fighter in fighters:
        matches = fighter.matches
        points = 0
        for match in matches:
            if match.w_l == "W":
                if match.method.startswith("Pts:"):
                    points += 2
                elif match.method in ["Referee Decision", "Advantages", "DQ"]:
                    points += 1
                else:
                    points += 3
            if match.w_l == "L":
                if match.method.startswith("Pts:"):
                    points -= 2
                elif match.method in ["Referee Decision", "Advantages", "DQ"]:
                    points -= 1
                else:
                    points -= 3
        fighter_scores.append({"fighter": fighter.name, "score": points})
    return sorted(fighter_scores, key=lambda x: x["score"], reverse=True)
