# from rest_api import get_student,app
# from decode import get_user
# from student import student_list,student
# import pytest_mock
# import json
# import requests_mock
# from auth import login

    
# def test_login_successfull(mocker,requests_mock):
    
#     req = mocker.Mock()
#     req.method = 'POST'
#     req.POST = {'username': 'uname', 'password': 'pass12343#12'}
#     req.status_code=201
#     fake_res={"response":"user logged in !"}
#     req.json=mocker.Mock(return_value=fake_res)
#     mocker.patch("auth.login",return_value=fake_res)
#     assert fake_res["response"]=="user logged in !"
    
# def test_login_failed(mocker):
#     req = mocker.Mock()
#     req.method = 'POST'
#     req.POST = {'username': 'uname', 'password': 'wrongpass'}
#     req.status_code=201
#     fake_res={"response":"invalid login credentials !"}
#     req.json=mocker.Mock(return_value=fake_res)
#     mocker.patch("auth.login",return_value=fake_res)
#     assert fake_res["response"]=="invalid login credentials !"
    