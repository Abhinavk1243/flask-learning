import pytest_mock
import json
import requests_mock
import admin
import rest_api
from rest_api import app,get_student




def test_admin_panel_expect200(mocker):
    fake_resp=mocker.Mock()
    fake_resp.method="GET"
    data={"Id": 1234, "username": "Abhinav kumar", "email_id": "abhinavk@gmail.com", "roles": "admin,user"}
    fake_resp.json=mocker.Mock(return_value=data)
    fake_resp.status_code=200
    mocker.patch("admin.admin_panel",return_value=data)
    response_text=fake_resp.json(key='value')
    assert fake_resp.status_code==200
    assert response_text["Id"]==data["Id"]
    assert response_text["username"]==data["username"]
    assert response_text["email_id"]==data["email_id"] 
    assert response_text["roles"]==data["roles"] 
    
    
# def test_get_updated_issues_one_page():
    
    
#     mock_response = [{'expand': 'operations,versionedRepresentations,editmeta,changelog,renderedFields', 'id': '10005',

#          'self': 'https://jira_url/rest/api/2/issue/10005', 'key': 'MYB-5'},

#         {'expand': 'operations,versionedRepresentations,editmeta,changelog,renderedFields', 'id': '10004',

#          'self': 'https://jira_url/rest/api/2/issue/10004', 'key': 'MYB-4'}]
#     expected_result = [

#         {'expand': 'operations,versionedRepresentations,editmeta,changelog,renderedFields', 'id': '10005',

#          'self': 'https://jira_url/rest/api/2/issue/10005', 'key': 'MYB-5'},

#         {'expand': 'operations,versionedRepresentations,editmeta,changelog,renderedFields', 'id': '10004',

#          'self': 'https://jira_url/rest/api/2/issue/10004', 'key': 'MYB-4'}]
#     with requests_mock.Mocker() as m:
#         m.register_uri('GET', '/student', text=json.dumps(mock_response))
#         with app.app_context():
#             response =get_student()
#     print("==+==+"*5)
#     print(response.json)
#     assert expected_result==response.json