import requests


class API_task_manager():
    def __init__(self):
        self.url = 'http://localhost:8000'

    def display(self, res):
        if res.status_code != 500:
            try:
                return {'status_code': res.status_code, 'res': res.json()}
            except:
                return {'status_code': res.status_code, 'res': res.text}

    def create_task(self, params):
        res = requests.get(f'{self.url}/create_task', params=params)
        return self.display(res)

    def get_task(self, params):
        res = requests.get(f'{self.url}/get_task', params=params)
        return self.display(res)

    def get_list_task(self):
        res = requests.get(f'{self.url}/get_list_task')
        return self.display(res)

    def update_task(self, params):
        res = requests.get(f'{self.url}/update_task', params=params)
        return self.display(res)

    def delete_task(self, params):
        res = requests.get(f'{self.url}/delete_task', params=params)
        return self.display(res)

    def clear_db(self):
        tasks = self.get_list_task()
        if isinstance(tasks.get('res'), list):
            for task in tasks.get('res'):
                self.delete_task({'id': task.get('id')})


api = API_task_manager()


def test_create_task():
    api.clear_db()

    params = {
        'name': 'Блины классические',
        'description': '1. В миску влить молоко и воду, всыпать сахар, соль, хорошо размешать. '
                       '2. Добавить яйца, тщательно взбить венчиком. '
                       '3. Постепенно всыпать просеянную муку, взбивая тесто венчиком.',
        'status': 'created'
    }

    # Test valid statuses
    valid_statuses = ['created', 'in progress', 'completed']
    for status in valid_statuses:
        params['status'] = status
        res = api.create_task(params)
        assert res['status_code'] == 200
        assert res['res']['name'] == params['name']
        assert res['res']['description'] == params['description']
        assert res['res']['status'] == status

    # Test invalid status
    params['status'] = 'invalid_status'
    res = api.create_task(params)
    assert res['status_code'] == 404
    assert res['res']['detail'] == 'the status is invalid'


def test_get_task():
    api.clear_db()

    # Create test task
    create_params = {
        'name': 'Тестовое задание',
        'description': 'Описание тестового задания',
        'status': 'created'
    }
    created_task = api.create_task(create_params)['res']

    # Test getting the task
    get_res = api.get_task({'id': created_task['id']})
    assert get_res['status_code'] == 200
    assert get_res['res'] == created_task

    # Test getting non-existent task
    non_existent_res = api.get_task({'id': 'non-existent-id'})
    assert non_existent_res['status_code'] == 404
    assert non_existent_res['res'] == {'detail': 'the id is invalid'}


def test_get_list_task():
    api.clear_db()

    # Check empty database
    empty_list = api.get_list_task()
    assert empty_list['status_code'] == 200
    assert empty_list['res'] == []

    # Create test tasks
    tasks_data = [
        {
            'name': 'Задача 1',
            'description': 'Описание задачи 1',
            'status': 'created'
        },
        {
            'name': 'Задача 2',
            'description': 'Описание задачи 2',
            'status': 'in progress'
        }
    ]

    created_tasks = []
    for task_data in tasks_data:
        res = api.create_task(task_data)
        created_tasks.append({
            'id': res['res']['id'],
            'name': task_data['name'],
            'status': task_data['status'],
            'description': f"{task_data['description'][:25]}..."
        })

    # Check list with tasks
    list_res = api.get_list_task()
    assert list_res['status_code'] == 200
    assert len(list_res['res']) == 2
    assert list_res['res'] == created_tasks


def test_update_task():
    api.clear_db()

    # Create test task
    create_params = {
        'name': 'Исходное название',
        'description': 'Исходное описание задачи',
        'status': 'created'
    }
    task = api.create_task(create_params)['res']

    # Test valid status transitions
    transitions = [
        ('created', True),
        ('in progress', True),
        ('in progress', True),
        ('created', False),
        ('completed', True),
        ('completed', True),
        ('in progress', False),
        ('created', False),
    ]

    for status, should_succeed in transitions:
        # Test transition
        update_res = api.update_task({'id': task['id'], 'status': status})

        if should_succeed:
            assert update_res['status_code'] == 200
            assert update_res['res']['status'] == status
        else:
            assert update_res['res'] == {'detail':'the parameters are not valid'}

    # Test updating name and description
    update_res = api.update_task({
        'id': task['id'],
        'name': 'Новое название',
        'description': 'Новое описание'
    })

    assert update_res['status_code'] == 200
    assert update_res['res']['name'] == 'Новое название'
    assert update_res['res']['description'] == 'Новое описание'

    # Test updating non-existent task
    non_existent_res = api.update_task({
        'id': 'non-existent-id',
        'name': 'Новое название'
    })
    assert non_existent_res['status_code'] == 404


def test_delete_task():
    api.clear_db()

    # Create test task
    create_params = {
        'name': 'Задача для удаления',
        'description': 'Описание задачи для удаления',
        'status': 'created'
    }
    task = api.create_task(create_params)['res']

    # Verify task exists
    get_res = api.get_task({'id': task['id']})
    assert get_res['status_code'] == 200
    assert get_res['res'] is not None

    # Delete the task
    delete_res = api.delete_task({'id': task['id']})
    assert delete_res['status_code'] == 200
    assert delete_res['res']['id'] == task['id']

    # Verify task no longer exists
    get_res_after_delete = api.get_task({'id': task['id']})
    assert get_res_after_delete['status_code'] == 404
    assert get_res_after_delete['res'] == {'detail': 'the id is invalid'}

    # Test deleting non-existent task
    non_existent_res = api.delete_task({'id': 'non-existent-id'})
    assert non_existent_res['status_code'] == 404
    assert non_existent_res['res'] == {'detail': 'the id is invalid'}