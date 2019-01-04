from google.cloud import bigquery


def congress_id_from_year(year):
    return int((year - 2011) / 2 + 112)


def get_gcp_vote_schema():
    return [
        bigquery.SchemaField('dw_nominate', 'FLOAT'),
        bigquery.SchemaField('member_id', 'STRING'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('party', 'STRING'),
        bigquery.SchemaField('state', 'STRING'),
        bigquery.SchemaField('vote_position', 'STRING'),
        bigquery.SchemaField('chamber', 'STRING'),
        bigquery.SchemaField('congress', 'INTEGER'),
        bigquery.SchemaField('session', 'INTEGER'),
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('time', 'TIME'),
        bigquery.SchemaField('roll_call', 'INTEGER'),
        bigquery.SchemaField('question', 'STRING'),
        bigquery.SchemaField('description', 'STRING')
    ]
