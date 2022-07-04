from goals.models import BoardParticipant

import pytest

"""
@pytest.mark.django_db
def test_category_create(client, get_token, board_factory, category_factory):
    
    board = board_factory(title='test_title')
    board_participant = BoardParticipant.objects.create(user=get_token[0], board=board)
    
    data = {'title': 'test-category_title', 'user': get_token[0], 'board': board.id}
    
    request = client.post('/goals/goal_category/create', data=data, format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    
    pk = request.data.get('id')
    response = client.get(f"/goals/goal_category/{pk}", format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert request.status_code == 201
    assert request.data.get('title') == data['title']
    
    assert response.status_code == 200
    assert response.data.get('title') == data['title']
"""    


@pytest.mark.django_db
def test_category_list(client, get_token, board_factory, category_factory):
    data_len = 10
    board = board_factory(title='test_title')
    board_participant = BoardParticipant.objects.create(user=get_token[0], board=board) # noqa F841
    
    category = category_factory.create_batch(size=data_len, title='test-category_title', user=get_token[0], board=board) # noqa F841

    response = client.get('/goals/goal_category/list', format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert response.status_code == 200
    assert len(response.data) == data_len
    
    for item in response.data:
        assert item.get('title') == 'test-category_title'
