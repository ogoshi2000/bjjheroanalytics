from flask.blueprints import Blueprint
from app.models import Match, Fighter, db
from sqlalchemy import func, case, desc, text

bjj_ranking = Blueprint("bjj_ranking", __name__, template_folder="templates")


@bjj_ranking.route("/score-by-wins", methods=["GET"])
def get_score_by_wins():
    try:
        score = (
            db.session.query(
                func.sum(
                    case((Match.w_l == "W", 1), (Match.w_l == "L", -1), else_=0)
                ).label("score"),
                Fighter.name,
                func.count(Match.id).label("matches"),
            )
            .join(Fighter, Fighter.id == Match.fighter_id)
            .group_by(Fighter.name)
            .order_by(desc("score"))
            .all()
        )
        return [{"rank":rank+1,"fighter": fighter.name, "score": fighter.score, "matches":fighter.matches} for rank,fighter in  enumerate(score)]
    except Exception as e:
        return str(e), 500


@bjj_ranking.route("/score-by-method", methods=["GET"])
def get_score_by_method():
    def calculate_method():
        stmnt = case(
            (
                text(
                    "Match.w_l = 'W' AND Match.method IN ('Referee Decision','Advantages','DQ','Pen','N/A')"
                ),
                1,
            ),
            (text("Match.w_l = 'W' AND Match.method LIKE 'Pts:%'"), 2),
            (text("Match.w_l = 'W'"), 3),
            (
                text(
                    "Match.w_l = 'L' AND Match.method IN ('Referee Decision','Advantages','DQ','Pen','N/A')"
                ),
                -1,
            ),
            (text("Match.w_l = 'L' AND Match.method LIKE 'Pts:%'"), -2),
            (text("Match.w_l = 'L'"),-3),
            else_=0,
        )

        return stmnt

    try:
        score = (
            db.session.query(
                Fighter.name,
                func.sum(calculate_method()).label("score"),
                func.count(Match.id).label("matches"),
            )
            .select_from(Match)
            .join(Fighter, Fighter.id == Match.fighter_id)
            .group_by(Fighter.name)
            .order_by(desc("score"))
            .all()
        )
        return [{"rank":rank+1,"fighter": fighter.name, "score": fighter.score, "matches":fighter.matches} for rank,fighter in  enumerate(score)]

    except Exception as e:
        return str(e), 500
