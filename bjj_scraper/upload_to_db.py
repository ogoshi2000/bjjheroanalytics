import json
import requests


def upload_fighters_to_db():
    with open("statistics.json") as f:
        data = json.load(f)
        data =[fighter['Name'] for fighter in data]
    
    requests.post("http://localhost:5000/fighters/", json={"fighter": data})

def upload_matches_to_db():
    matches = []
    with open("statistics.json") as f:
        data = json.load(f)
        for fighter in data:
            for match in fighter["TableData"]:
                match = { **{"name": fighter["Name"]}, **match }
                matches.append(match)
    print(matches)
    requests.post("http://localhost:5000/matches/", json=matches)
       
if __name__ == "__main__":
    upload_matches_to_db()
    # upload_fighters_to_db()