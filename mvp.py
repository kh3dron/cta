from flask import Flask, jsonify, request

app = Flask(__name__)


election_results = {
    "Pennsylvania": {
        "Chester": {
            "Democrats" :{
                "Humphrey ": 100,
                "McGovern": 50
            },
            "Republicans" :{
                "Nixon": 200,
                "Ashbrook": 2,
                "McCloskey": 1
            }
        }
    }
}

election_results_multistate = {
    "Pennsylvania": {
        "Chester": {
            "Democrats" :{
                "Humphrey ": 100,
                "McGovern": 50
            },
            "Republicans" :{
                "Nixon": 200,
                "Ashbrook": 2,
                "McCloskey": 1
            }
        }
    },
    "New York": {
        "Erie": {
            "Democrats" :{
                "Humphrey ": 235,
                "McGovern": 521
            },
            "Republicans" :{
                "Nixon": 587,
                "Ashbrook": 963,
                "McCloskey": 123
            }
        },
        "Kings": {
            "Democrats" :{
                "Humphrey ": 147,
                "McGovern": 785
            },
            "Republicans" :{
                "Nixon": 258,
                "Ashbrook": 789,
                "McCloskey": 456
            }
        }
    },
    "California": {
        "San Francisco": {
            "Democrats" :{
                "Humphrey ": 147,
                "McGovern": 785
            },
            "Republicans" :{
                "Nixon": 258,
                "Ashbrook": 789,
                "McCloskey": 456
            }
        }
    }
}

# 
def get_state_winner(data, state):
    state_results = data.get(state, {})
    votes = {}
    for county in state_results:
        for party in state_results[county]:
            for candidate in state_results[county][party]:
                if candidate in votes:
                    votes[candidate] += state_results[county][party][candidate]
                else:
                    votes[candidate] = state_results[county][party][candidate]

    winner = max(votes, key=votes.get)
    if list(votes.values()).count(votes[winner]) > 1:
        return "Tie between " + ", ".join([candidate for candidate in votes if votes[candidate] == votes[winner]])
    return winner

def get_all_state_winners(data):
    state_winners = {}
    for state in data:
        state_winners[state] = get_state_winner(data, state)

    return state_winners

def get_overall_winner(data):
    votes = {}
    for state in data:
        for county in data[state]:
            for party in data[state][county]:
                for candidate in data[state][county][party]:
                    if candidate in votes:
                        votes[candidate] += data[state][county][party][candidate]
                    else:
                        votes[candidate] = data[state][county][party][candidate]

    winner = max(votes, key=votes.get)

    if list(votes.values()).count(votes[winner]) > 1:
        return "Tie between " + ", ".join([candidate for candidate in votes if votes[candidate] == votes[winner]])
    else:
        return winner


@app.route('/state_winner', methods=['GET'])
def state_winner():
    state = request.args.get('state')
    if state:
        return jsonify({state: get_state_winner(election_results_multistate, state)})
    else:
        return jsonify({"error": "Please provide a 'state' parameter."}), 400

@app.route('/state_breakdown', methods=['GET'])
def all_state_winners():
    return jsonify(get_all_state_winners(election_results_multistate))

@app.route('/overall_winner', methods=['GET'])
def overall_winner():
    return jsonify(get_overall_winner(election_results_multistate))

if __name__ == '__main__':
    app.run(debug=True, port=3333)