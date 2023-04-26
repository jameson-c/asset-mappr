import pandas as pd
from sqlalchemy import create_engine
import os
import json


con_string = os.getenv('DB_URI')

master_category = pd.read_sql_table('categories_master', con=con_string)
master_categories = master_category['category'].values.tolist()
master_categories_desc = master_category['description'].values.tolist()

# Load the values master list
master_value_tags = pd.read_sql_table('values_master', con=con_string)
tagList_pos = master_value_tags.loc[master_value_tags['value_type']
                                    == 'Positive', 'value'].tolist()
tagList_neg = master_value_tags.loc[master_value_tags['value_type']
                                    == 'Negative', 'value'].tolist()
master_value_tags = [i for i in master_value_tags['value']]


# Load the communities master list
master_communities = pd.read_sql_table(
    'communities_master', con=con_string)


community_geo_id = '4250408'
# Load the main assets database
query = '''SELECT * FROM assets 
            WHERE community_geo_id = {}'''.format(community_geo_id)

df_cnm = pd.read_sql(query, con=con_string)

# Load the asset-categories mapping database for the relevant asset IDs
# query = '''SELECT * FROM asset_categories
#             WHERE asset_id IN
#                 (SELECT asset_id FROM assets
#                 WHERE community_geo_id = {})
#             '''.format(community_geo_id)


# load survey questions
query = '''SELECT questions FROM survey_table'''
survey_questions = pd.read_sql(query, con=con_string)

out = survey_questions.to_json(orient='records')
data = json.loads(out)
q_value = []
for i in data:
    q_dict = i['questions']
    temp = json.loads(q_dict)
    for j in range(1, 10):
        if str(j) in q_dict:
            q_value.append(temp[str(j)]['question'])
        else:
            q_value.append(None)

# load survey response
query = '''SELECT response FROM survey_response 
            WHERE survey_date >= '2023-03-24 00:00:00' AND survey_date <= '2023-03-24 23:59:59' '''
survey_responses = pd.read_sql(query, con=con_string)

out = survey_responses.to_json(orient='records')
data = json.loads(out)
response_values = []
for i in data:
    response_dict = i["response"]
    response_value = []
    for j in range(1, 10):
        if str(j) in response_dict:
            temp = json.loads(response_dict[str(j)])
            response_value.append(temp['value'])
        else:
            response_value.append(None)
    response_values.append(response_value)

data_dict = {}
for col in range(len(q_value)):
    col_name = q_value[col]
    data_dict[col_name] = [lst[col] for lst in response_values]
survey = pd.DataFrame(data_dict)
# print(survey.columns)
df_placeholder = pd.DataFrame(columns=['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5'],
                              index=range(1, 10))
print(survey)
