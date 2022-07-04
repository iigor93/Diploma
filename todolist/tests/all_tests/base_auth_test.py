def test_no_auth_goal(client):
    response = client.get("/goals/goal/list")
    
    assert response.status_code == 403


def test_no_auth_board(client):
    response = client.get("/goals/board/list")
    
    assert response.status_code == 403


def test_no_auth_category(client):
    response = client.get("/goals/goal_category/list")
    
    assert response.status_code == 403
    

def test_auth_goal_list(client, get_token):
    response = client.get("/goals/goal/list", HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert response.status_code == 200


def test_auth_goal_board(client, get_token):
    response = client.get("/goals/board/list", HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert response.status_code == 200


def test_auth_goal_category(client, get_token):
    response = client.get("/goals/goal_category/list", HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert response.status_code == 200


def test_api_swagger(client):
    response = client.get('/api/schema/swagger-ui/')
    
    assert response.status_code == 200
