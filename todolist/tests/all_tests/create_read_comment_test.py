from goals.models import BoardParticipant

import pytest


"""
@pytest.mark.django_db
def test_comment_create(client, get_token, board_factory, category_factory, goal_factory, comment_factory):
    
    board = board_factory(title='test_title')
    board_participant = BoardParticipant.objects.create(user=get_token[0], board=board)
    category = category_factory(title='test-category_title', user=get_token[0], board=board)
    goal = goal_factory(title='test-goal_title', user=get_token[0], category=category)
    
    data = {'text': 'text_comment', 'user': get_token[0], 'goal': goal.id}
    
    request = client.post('/goals/goal_comment/create', data=data, format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    pk = request.data.get('id')
    response = client.get(f"/goals/goal_comment/{pk}", format='json', HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert request.status_code == 201
    assert request.data.get('text') == data['text']
    
    assert response.status_code == 200
    assert response.data.get('text') == data['text']
"""


@pytest.mark.django_db
def test_comment_list(client, get_token, board_factory, category_factory, goal_factory, comment_factory):
    data_len = 10
    board = board_factory(title='test_title')
    board_participant = BoardParticipant.objects.create(user=get_token[0], board=board)  # noqa F841
    category = category_factory(title='test-category_title', user=get_token[0], board=board)
    goal = goal_factory(title='test-goal_title', user=get_token[0], category=category)
    
    comment = comment_factory.create_batch(size=data_len,   # noqa F841
                                           text='test-comment_text',
                                           user=get_token[0],
                                           goal=goal)

    response = client.get('/goals/goal_comment/list',
                          format='json',
                          HTTP_AUTHORIZATION='Token ' + get_token[1])
    
    assert response.status_code == 200
    assert len(response.data) == data_len
    
    for item in response.data:
        assert item.get('text') == 'test-comment_text'
