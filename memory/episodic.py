import json
from datetime import datetime


EPISODIC_FILE = "memory/episodic_log.json"


def log_episode(query, outcome, strategy):

    episode = {
        "timestamp": str(datetime.now()),
        "query": query,
        "outcome": outcome,
        "strategy": strategy
    }

    try:

        with open(EPISODIC_FILE, "r") as f:
            data = json.load(f)

    except:
        data = []

    data.append(episode)

    with open(EPISODIC_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return "Episode logged successfully."