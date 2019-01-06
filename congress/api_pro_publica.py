import pandas as pd
import requests
import json

# pro publica API documentation here: https://propublica.github.io/congress-api-docs/
# Hold API key in a separate file
PRO_PUBLICA_API_KEY = json.load(open('pro_publica_api.json'))


# Function for loading vote meta data_legacy_gov_track (name, who won, ID, house, session, etc), from Pro Publica API
def load_vote_meta_data_pro_publica(chamber, year):
    def get_one_month(c, y, m):
        url = "https://api.propublica.org/congress/v1/{}/votes/{}/{}.json".format(c, y, m)
        # print url
        json_response = requests.get(url, headers=PRO_PUBLICA_API_KEY).json()
        return pd.DataFrame(json_response.get("results", {"votes": None})["votes"])

    data = map(lambda m: get_one_month(chamber, year, m+1), range(12))
    data = pd.DataFrame(pd.concat(data))
    index_cols = ['chamber', 'congress', 'session', 'date', 'time', 'roll_call', 'question', 'description']
    data = data.sort_values(index_cols).set_index(index_cols)
    data = pd.DataFrame.from_records(list(data.index.values), columns=data.index.names)
    return data


def retrieve_vote_pro_publica(vote):
    # Note - session format for Pro Publica is 1 or 2 for odd- and even-numbered years, respectively.
    print "Retrieving vote:", vote
    url = "https://api.propublica.org/congress/v1/{}/{}/sessions/{}/votes/{}.json".format(
        vote['congress'], vote['chamber'], vote['session'], vote['roll_call'])
    # print url
    json_result = requests.get(url, headers=PRO_PUBLICA_API_KEY).json()
    # print json["results"]["votes"]["vote"]["positions"]
    result = pd.DataFrame(json_result["results"]["votes"]["vote"]["positions"])

    if 'dw_nominate' in result:
        result['dw_nominate'] = pd.to_numeric(result['dw_nominate'])  # Need to handle years with dw_nominate="None"
    else:
        result['dw_nominate'] = None

    result['chamber'] = vote["chamber"]
    result['congress'] = vote["congress"]
    result['session'] = vote["session"]
    result['date'] = vote["date"]
    result['time'] = vote["time"]
    result['roll_call'] = json_result["results"]["votes"]["vote"]['roll_call']
    result['question'] = json_result["results"]["votes"]["vote"]['question']
    result['description'] = json_result["results"]["votes"]["vote"]['description']
    return result
