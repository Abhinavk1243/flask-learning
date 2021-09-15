
import pytest_mock
import json
import requests_mock
import student

def test_student_list_expect200(mocker):
    fake_resp=mocker.Mock()
    fake_resp.method="GET"
    data={"date_created": "2021-09-09", "student_id": 52, "student_name": "rohan", "student_age": 23}
    fake_resp.json=mocker.Mock(return_value=data)
    fake_resp.status_code=200
    mocker.patch("student.student_list",return_value=data)
    response_text=fake_resp.json(key='value')
    assert fake_resp.status_code==200
    assert response_text["date_created"]==data["date_created"]
    assert response_text["student_id"]==data["student_id"]
    assert response_text["student_name"]==data["student_name"] 
    assert response_text["student_age"]==data["student_age"] 
    
def test_student_list_expect400(mocker):
    fake_resp=mocker.Mock()
    params={"student_id":1}
    fake_resp.query_param=params
    fake_resp.status_code=400
    resp={"error":f"record at {list(params.keys())[0]}={params[list(params.keys())[0]]} not found"}
    fake_resp.json=mocker.Mock(return_value=resp)
    mocker.patch("student.student_list",return_value=resp)
    response_text=fake_resp.json(key='value')
    assert response_text["error"]==resp["error"]
    
    
def test_create_student_expect200(mocker):
    req = mocker.Mock()
    req.method = 'POST'
    data={'student_name': 'abhinav', 'student_age': 21}
    req.POST = data
    req.status_code=201
    fake_res={"response_msg":"student record successfully created",
        "data":{"date_created":"2021-09-12","student_id":1342,"student_name":"abhinav","student_age":21}}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.create_student",return_value=fake_res)
    res=req.json(key="value")
    assert res["response_msg"]==fake_res["response_msg"]
    assert res["data"]["student_name"]==fake_res["data"]["student_name"]
    assert res["data"]["student_age"]==fake_res["data"]["student_age"]
    
    
def test_create_student_expect400(mocker):
    req = mocker.Mock()
    req.method = 'POST'
    data={'student_name': 'abhinav', 'student_age': 21}
    req.POST = data
    req.status_code=400
    example_data={"student_name":"name","student_age":54}
    fake_res={"error":"data contain wrong keys","sample_data":example_data}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.create_student",return_value=fake_res)
    res=req.json(key="value")
    assert res["error"]==fake_res["error"]
    
def test_create_student_expect500(mocker):
    req=mocker.Mock()
    req.method = 'POST'
    data={'student_name': 'abhinav', 'student_age': 21}
    req.POST = data
    req.status_code=500
    fake_res={"error" : "internal server error"}
    req.json=mocker.Mock(return_value=fake_res)
    res=req.json(key='value')
    
    mocker.patch("student.create_student",return_value=fake_res)
    assert res["error"]==res["error"]
    
def test_remove_student_200(mocker):
    req=mocker.Mock()
    req.method ="DELETE" 
    data = {"student_id":32}
    req.DELETE = data
    req.status_code=200
    student={"date_created" : "2021-09-09","student_id" :32,"student_name":"Abhinav","student_age":22}
    fake_res={"response":"student is successfully removed from database","removed_student_record":student}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.remove_student",return_value=fake_res)
    res=req.json(key="value")
    assert res["response"]==fake_res["response"]
    
def test_remove_student_expect400(mocker):
    req=mocker.Mock()
    req.method ="DELETE" 
    data = {"student_id":33}
    req.DELETE = data
    req.status_code=400
    fake_res={"error":"student with id 33 not exist"}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.remove_student",return_value=fake_res)
    res=req.json(key="value")
    assert res["error"]==fake_res["error"]
    
def test_remove_student_expect500(mocker):
    req=mocker.Mock()
    req.method ="DELETE" 
    data = {"student_id":33}
    req.DELETE = data
    req.status_code=500
    fake_res={"error" : "internal server error"}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.remove_student",return_value=fake_res)
    res=req.json(key='value')
    assert res["error"]==res["error"]
    
def test_student_update_expect200(mocker):
    req = mocker.Mock()
    req.method = 'PUT'
    data={'student_id':1342,'student_name': 'abhinav', 'student_age': 21}
    req.PUT = data
    req.status_code=200 
    fake_res={"response_msg":"student record successfully updated",
        "data":{"date_created":"2021-09-12","student_id":1342,"student_name":"abhinav","student_age":21}}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.student_update",return_value=fake_res)
    res=req.json(key="value")
    assert res["response_msg"]=="student record successfully updated"
    assert res["data"]["student_name"]==data["student_name"]
    assert res["data"]["student_id"]==data["student_id"]
    assert res["data"]["student_age"]==data["student_age"]
    
    
def test_student_update_expect400(mocker):
    req = mocker.Mock()
    req.method = 'PUT'
    data={'student_id':1324,'student_name': 'abhinav', 'student_age': 21}
    req.PUT = data
    req.status_code=400
    
    fake_res={"error" : "student with id 1324 not exist"}
    req.json=mocker.Mock(return_value=fake_res)
    mocker.patch("student.student_update",return_value=fake_res)
    res=req.json(key="value")
    assert res["error"]==fake_res["error"]
    

def test_student_update_expect500(mocker):
    req = mocker.Mock()
    req.method = 'PUT'
    data={'student_id':1324,'student_name': 'abhinav', 'student_age': 21}
    req.PUT = data
    req.status_code=500
    res={"error" : "internal server error"}
    req.json=mocker.Mock(return_value=res)
    response_text=req.json(key='value')
    mocker.patch("student.student_update",return_value=res)
    assert response_text["error"]==res["error"]