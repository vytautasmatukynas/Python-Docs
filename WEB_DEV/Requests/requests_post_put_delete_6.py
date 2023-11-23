import requests
from datetime import datetime

# request.get() - ask for piece of data from server and get it.
# request.post() - give data to server. Create piece of data.
# request.put() - change an existing piece of data.
# request.delete() - delete an existing piece of data.

USERNAME = "xxxxx"
TOKEN = "xxxxxx"
GRAPH_ID = "xxxxxx"

headers = {
         "X-USER-TOKEN": TOKEN
}

pixela_end_point = "https://pixe.la/v1/users"
param = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

############################################ POST
# create username and token in pixela using requests.post
response = requests.post(url=pixela_end_point, json=param)
print(response.text)

#################################### POST
# create graph
# graph_end_point = f"{pixela_end_point}/{USERNAME}/graphs"
#
# param_graph = {
#     "id": "xxxxx",
#     "name": "lets do it",
#     "unit": "Hour",
#     "type": "float",
#     "color": "shibafu"
# }
#
# response = requests.post(url=graph_end_point, json=param_graph, headers=headers)
#
# print(response.text)

######################################################## POST
# dot_end_point = f"{pixela_end_point}/{USERNAME}/graphs/{GRAPH_ID}"
#
# date_now = datetime.now()
# DATE = date_now.strftime("%Y%m%d")
#
# param_dot = {
#     "date": DATE,
#     "quantity": "2",
# }
#
# response = requests.post(url=dot_end_point, json=param_dot, headers=headers)
# print(response.text)

############################################ PUT
# date_now = datetime.now()
# DATE = date_now.strftime("%Y%m%d")
#
# dot_update_end_point = f"{pixela_end_point}/{USERNAME}/graphs/{GRAPH_ID}/{DATE}"
#
# param_dot_update = {
#     "quantity": "2",
# }
#
# response = requests.put(url=dot_update_end_point, json=param_dot_update, headers=headers)
# print(response.text)

# ###################################################### DELETE
# date_now = datetime.now()
# DATE = date_now.strftime("%Y%m%d")
#
# dot_delete_end_point = f"{pixela_end_point}/{USERNAME}/graphs/{GRAPH_ID}/{DATE}"
#
# response = requests.delete(url=dot_delete_end_point, headers=headers)
# print(response.text)
