import pytest
from datetime import datetime
from django.utils import timezone

from goals.models import BoardParticipant


@pytest.mark.django_db
def test_category_crud_reader(client, get_token, board_factory):
    token = 'Token ' + get_token[1]
    current_user = get_token[0]
    
    owner_token = 'Token ' + get_token[3]
    owner_user = get_token[2]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user, board=board, role=BoardParticipant.Role.READER)
    board_participant = BoardParticipant.objects.create(user=owner_user, board=board, role=BoardParticipant.Role.OWNER)
    
    data = {'title': 'test_category_title', 'user': owner_user, 'board': board.id}
    reader_data = {'title': 'test_category_title', 'user': current_user, 'board': board.id}
    
    create_request = client.post('/goals/goal_category/create', data=reader_data, HTTP_AUTHORIZATION=token)
    owner_request = client.post('/goals/goal_category/create', data=data, HTTP_AUTHORIZATION=owner_token) 
    
    pk = owner_request.data.get('id')
    response = client.get(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {'title': 'updated_title'}
    update_request = client.patch(f"/goals/goal_category/{pk}",
                                  content_type='application/json',
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = client.delete(f'/goals/goal_category/{pk}', HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 403
    
    assert response.status_code == 200
    assert response.data.get('title') == data['title']
    
    assert update_request.status_code == 403
    
    assert delete_request.status_code == 403

  
@pytest.mark.django_db
def test_goal_crud_reader(client, get_token, board_factory, category_factory):
    token = 'Token ' + get_token[1]
    current_user = get_token[0]
    
    owner_token = 'Token ' + get_token[3]
    owner_user = get_token[2]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user, board=board, role=BoardParticipant.Role.READER)
    board_participant = BoardParticipant.objects.create(user=owner_user, board=board, role=BoardParticipant.Role.OWNER)
    category = category_factory(user=owner_user, board=board)
    
    
    data = {'title': 'test_goal_title', 
            'user': owner_user, 
            'category': category.id,
            'description': 'some description',
            'due_date': datetime.now(tz=timezone.utc)}
    
    reader_data = {'title': 'test_goal_title', 
            'user': current_user, 
            'category': category.id,
            'description': 'some description',
            'due_date': datetime.now(tz=timezone.utc)}
    
    
    create_request = client.post('/goals/goal/create', data=data, HTTP_AUTHORIZATION=token)
    owner_request = client.post('/goals/goal/create', data=data, HTTP_AUTHORIZATION=owner_token)
    
    pk = owner_request.data.get('id')
    response = client.get(f"/goals/goal/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {'title': 'updated_title'}
    update_request = client.patch(f"/goals/goal/{pk}",
                                  content_type='application/json',
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = client.delete(f'/goals/goal/{pk}', HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 403
    
    assert response.status_code == 200
    assert response.data.get('title') == data['title']
    
    assert update_request.status_code == 403
    
    assert delete_request.status_code == 403


  
@pytest.mark.django_db
def test_comment_crud_reader(client, get_token, board_factory, category_factory, goal_factory):
    token = 'Token ' + get_token[1]
    current_user = get_token[0]
    
    owner_token = 'Token ' + get_token[3]
    owner_user = get_token[2]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user, board=board, role=BoardParticipant.Role.READER)
    board_participant = BoardParticipant.objects.create(user=owner_user, board=board, role=BoardParticipant.Role.OWNER)
    category = category_factory(user=owner_user, board=board)
    goal = goal_factory(user=owner_user, category=category)
    
    data = {'text': 'test_text_comment', 
            'user': current_user, 
            'goal': goal.id}
            
    owner_data = {'text': 'test_text_comment', 
            'user': owner_user, 
            'goal': goal.id}
    
    create_request = client.post('/goals/goal_comment/create', data=data, HTTP_AUTHORIZATION=token)
    owner_request = client.post('/goals/goal_comment/create', data=data, HTTP_AUTHORIZATION=owner_token)
    
    pk = owner_request.data.get('id')
    response = client.get(f"/goals/goal_comment/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {'text': 'updated_text'}
    update_request = client.patch(f"/goals/goal_comment/{pk}",
                                  content_type='application/json',
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = client.delete(f'/goals/goal_comment/{pk}', HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 403
    
    assert response.status_code == 200
    assert response.data.get('text') == data['text']
    
    assert update_request.status_code == 403
    
    assert delete_request.status_code == 403
