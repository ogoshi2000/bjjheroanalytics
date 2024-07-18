from flask.blueprints import Blueprint
from app.models import Match, Fighter

bjj_ranking = Blueprint("bjj_ranking", __name__, template_folder="templates")


def score_by_win(w_l):
    return 1 if w_l == "W" else -1 if w_l == "L" else 0


def score_by_method(w_l, method):
    if w_l == "W":
        if method in ["Referee Decision", "Advantages", "DQ"]:
            return 1
        elif method.startswith("Pts:"):
            return 2
        else:
            return 3
    elif w_l == "L":
        if method in ["Referee Decision", "Advantages", "DQ"]:
            return -1
        elif method.startswith("Pts:"):
            return -2
        else:
            return -3
    else:
        return 0


@bjj_ranking.route("/score-by-wins", methods=["GET"])
def get_score_by_wins():
    try:
        fighters = Fighter.query.join(Match, Fighter.id == Match.fighter_id).all()
        fighter_scores = [
            {
                "fighter": fighter.name,
                "score": sum(score_by_win(match.w_l) for match in fighter.matches),
            }
            for fighter in fighters
        ]
        return sorted(fighter_scores, key=lambda x: x["score"], reverse=True)

    except Exception as e:
        return str(e), 500


@bjj_ranking.route("/score-by-method", methods=["GET"])
def get_score_by_method():
    try:
        fighter_scores = []
        fighters = Fighter.query.join(Match, Fighter.id == Match.fighter_id).all()
        fighter_scores = [
            {
                "fighter": fighter.name,
                "score": sum(
                    score_by_method(match.w_l, match.method)
                    for match in fighter.matches
                ),
            }
            for fighter in fighters
        ]
        sorted_scores = sorted(fighter_scores, key=lambda x: x["score"], reverse=True)
        return sorted_scores
    except Exception as e:
        return str(e), 500
