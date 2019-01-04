import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
# Function for loading vote meta data_legacy_gov_track (name, who won, ID, house, session, etc), from Gov Track API
# gov track API Documentation here: https://www.govtrack.us/developers/api
# NOTE: Gov Track is being deprecated after the Summer 2017 recess.
def load_vote_meta_data_gov_track(congress, chamber, session):
    url = "https://www.govtrack.us/api/v2/vote/?congress={}&chamber={}&session={}&limit=5000".format(
        congress, chamber, session)
    json = requests.get(url).json()

    data = pd.DataFrame(json['objects'])
    data = data.sort_values('id').set_index(['id'])

    return data


def retrieve_vote_gov_track(vote):
    # VOTE_VOTER: For a given vote, list of people and voted values.
    url = "https://www.govtrack.us/api/v2/vote_voter/?vote={}&limit=441".format(vote)
    print "Loading vote", vote, "...",
    json = requests.get(url).json()

    print "found", len(json["objects"]), "vote objects...",

    if len(json["objects"]):
        data = map(lambda o: [o["person"]["name"], o["option"]["value"]], json["objects"])
        question = json["objects"][0]["vote"]["question"]
        data = pd.DataFrame(data, columns=["name", str(vote) + " " + question])
    else:
        print "vote", vote, "was empty."
        data = pd.DataFrame([], columns=["name", "vote {}".format(vote)])

    data.set_index(["name"], inplace=True)

    return data


def file_path(vote):
    return "data_legacy_gov_track/{}.csv".format(vote)


def cache_vote(vote):
    if not os.path.exists("data_legacy_gov_track"):
        print "Directory 'data_legacy_gov_track' not found - creating it."
        os.mkdir("data_legacy_gov_track")

    if os.path.isfile(file_path(vote)):
        print "Vote", vote, "already cached."
    else:
        data = retrieve_vote_gov_track(vote)
        data.to_csv(file_path(vote), sep="|", encoding='utf-8')
        print "Vote", vote, "has been cached."
