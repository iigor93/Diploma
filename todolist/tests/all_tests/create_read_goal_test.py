from goals.models import BoardParticipant

import pytest


"""
@pytest.mark.django_db
def test_goal_create(client, get_token, board_factory, category_factory, goal_factory):
    
    board = board_factory(title='test_title')
    board_participant = BoardParticipant.objects.create(user=get_token[0], board=board)
    category = category_factory(title='test-category_title', user=get_token[0], board=board)
    
    data = {'title': 'test-goal_title', 'user': get_token[0], 'category': category.id, 
        'description': 'some descripton', 'due_date': datetime.now(tz=timezone.utc)}
    
    request = client.post('/goals/goal/create', data=data, format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    pk = request.data.get('id')
    response = client.get(f"/goals/goal/{pk}", format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert request.status_code == 201
    assert request.data.get('title') == data['title']
    
    assert response.status_code == 200
    assert response.data.get('title') == data['title']
"""    


@pytest.mark.django_db
def test_goal_list(client, get_token, board_factory, category_factory, goal_factory):
    data_len = 10
    board = board_factory(title='test_title')
    board_participant = BoardParticipant.objects.create(user=get_token[0], board=board)  # noqa F841
    category = category_factory(title='test-category_title', user=get_token[0], board=board)
    
    goal = goal_factory.create_batch(size=data_len,  # noqa F841
                                     title='test-goal_title',
                                     user=get_token[0],
                                     category=category)

    response = client.get('/goals/goal/list', format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert response.status_code == 200
    assert len(response.data) == data_len
    
    for item in response.data:
        assert item.get('title') == 'test-goal_title'
