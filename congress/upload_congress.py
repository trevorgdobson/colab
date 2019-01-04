from api_pro_publica import *
from gcp_helpers import *
from datetime import *
from congress_helpers import *
import google.api_core.exceptions as exceptions

dataset_id = "congress"
table_prefix = "votes"
years = range(2000, 2019)
years.reverse()
# chambers = ['senate', 'house']
chambers = ['senate']

use_existing = True

for chamber in chambers:
    for year in years:
        table_id = "{}_{}_{}".format(table_prefix, year, chamber)

        if table_exists(dataset_id, table_id) and use_existing:
            print "\nTable", table_id, "already exists."
            continue
        else:
            print "\n\n"
            print "{}: Generating {}.{}".format(datetime.now(), dataset_id, table_id)
            print "{}: Loading meta-data...".format(datetime.now()),
            vote_meta_data = load_vote_meta_data_pro_publica(chamber, year)
            print "found", len(vote_meta_data), "votes."

            print "{}: Loading votes from API...".format(datetime.now())
            data = pd.DataFrame(pd.concat(map(retrieve_vote_pro_publica, vote_meta_data.to_dict('records'))))

            print "{}: Uploading data to GCP...".format(datetime.now())
            try:
                upload_data_frame_to_gcp(data, dataset_id, table_id, gcp_schema=get_gcp_vote_schema(chamber))
                print "{}: Load complete.".format(datetime.now())
            except exceptions.BadRequest as err:
                print err
            except requests.exceptions.ConnectionError as err:
                print err
