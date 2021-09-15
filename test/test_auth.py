
import rest_api
import requests_mock
# import pytest_mock

# from  student import student_list
    
def test_login_successfull(mocker,requests_mock):
    
    req = mocker.Mock()
    req.method = 'POST'
    req.content_type=="multipart/form-data"
    req.POST = {'username': 'uname', 'password': 'pass12343#12'}
    req.status_code=201
    fake_res={"response":"user logged in !"}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("auth.login",return_value=fake_res)
    res=req.json(key="value")
    assert res["response"]==fake_res["response"]
    
def test_login_failed(mocker):
    req = mocker.Mock()
    req.method = 'POST'
    req.content_type=="multipart/form-data"
    req.POST = {'username': 'uname', 'password': 'wrongpass'}
    req.status_code=400
    fake_res={"response":"invalid login credentials !"}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("auth.login",return_value=fake_res)
    res=req.json(key="value")
    assert res["response"]==fake_res["response"]
    
    


def test_signup_expect200(mocker):
    req = mocker.Mock()
    req.method = 'POST'
    req.content_type=="multipart/form-data"
    req.POST = {'username': 'uname', 'password': 'pass12343#12',"email":"abhinavk@gmail.com","upload_file":open('test_api.txt','rb')}
    file_name='test_api.txt'
    req.status_code=201
    fake_res={"message":"you are successfull registered !","user":{'username': 'uname', 'password': 'cww85r76762736t354trsg5sef5ef',"email":"abhinavk@gmail.com","filename":file_name}}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("auth.signup",return_value=fake_res)
    res=req.json(key="value")
    assert res["message"]==fake_res["message"]
    assert res["user"]["username"]==fake_res["user"]["username"]
    assert res["user"]["email"]==fake_res["user"]["email"]
    assert res["user"]["filename"]==fake_res["user"]["filename"]
    