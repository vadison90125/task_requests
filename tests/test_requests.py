from conftest import base_url
import requests
import allure
import json
import random


class TestRequestsCollections:

    @allure.feature("GET - /posts")
    @allure.story("Получение количества всех постов")
    def test_get_all_posts(self, base_url):
        url = base_url + '/posts'
        with allure.step("Отправка GET запроса"):
            response = requests.request("GET", url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка количества постов на значение 100"):
            response = response.json()
            assert len(response) == 100

    @allure.feature("GET - /posts")
    @allure.story("Получение одного поста по 'id'")
    def test_get_one_post(self, base_url):
        url = base_url + '/posts'
        response = requests.request("GET", url)
        count_posts = len(response.json())
        post_id = random.randint(1, count_posts)
        url = base_url + f'/posts/{post_id}'
        with allure.step("Отправка GET запроса"):
            response = requests.request('GET', url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step(f"Проверка 'id' поста на значение {post_id}"):
            response = response.json()
        assert response['id'] == post_id

    @allure.feature("GET - /posts")
    @allure.story("Попытка получения несуществующих постов (невалидные 'id')")
    def test_get_not_exist_posts(self, base_url):
        url = base_url + '/posts'
        with allure.step("Получение общего количества постов"):
            response = requests.request('GET', url)
            response = response.json()
            count_posts = len(response)
        url1 = base_url + f'/posts/{count_posts + 1}'
        url2 = base_url + f'/posts/0'
        url3 = base_url + f'/posts/-1'
        urls = [url1, url2, url3]
        with allure.step("Отправка GET запросов"):
            responses = []
            for url in urls:
                response = requests.request('GET', url)
                responses.append(response)
        with allure.step("Проверка статус кода отправленных запросов на значение 404"):
            for response in responses:
                assert response.status_code == 404

    @allure.feature("GET - /posts")
    @allure.story("Получение отфильтрованных постов по 'userId'")
    def test_get_filters_posts(self, base_url):
        url = base_url + '/posts?userId=1'
        with allure.step("Отправка GET запроса"):
            response = requests.request("GET", url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка количества отфильтрованных постов по 'userId' на значение 10"):
            response = response.json()
            assert len(response) == 10

    @allure.feature("GET - /posts")
    @allure.story("Получение одного поста (бизнес-логика)")
    def test_get_business_logic_post(self, base_url):
        url = base_url + f'/posts/100'
        with allure.step("Отправка GET запроса"):
            response = requests.request('GET', url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка бизнес-логики поста"):
            assert response.json() == {
                'body': 'cupiditate quo est a modi nesciunt soluta\n'
                        'ipsa voluptas error itaque dicta in\n'
                        'autem qui minus magnam et distinctio eum\n'
                        'accusamus ratione error aut',
                'id': 100,
                'title': 'at nam consequatur ea labore ea harum',
                'userId': 10}

    @allure.feature("POST - /posts")
    @allure.story("Создание поста")
    def test_create_post(self, base_url):
        url = base_url + '/posts/'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = json.dumps({
            'title': 'My cool post',
            'body': 'My cool message',
            'userID': 1
        })
        with allure.step("Отправка POST запроса"):
            response = requests.request('POST', url, headers=headers, data=data)
        with allure.step("Проверка статус кода на значение 201"):
            assert response.status_code == 201
        with allure.step("Проверка созданного поста"):
            assert response.json() == {
                'id': 101,
                'title': 'My cool post',
                'body': 'My cool message',
                'userID': 1
            }

    @allure.feature("POST - /posts")
    @allure.story("Создание поста без тела запроса")
    def test_create_without_body_post(self, base_url):
        url = base_url + '/posts/'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        with allure.step("Отправка POST запроса"):
            response = requests.request('POST', url, headers=headers)
        with allure.step("Проверка статус кода на значение 201"):
            assert response.status_code == 201
        with allure.step("Проверка созданного поста"):
            assert response.json() == {
                'id': 101
            }

    @allure.feature("PUT - /posts")
    @allure.story("Изменение существующего поста")
    def test_update_exist_post(self, base_url):
        url = base_url + '/posts/1'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = json.dumps({
            'title': 'My cool update',
            'body': 'My cool message update',
            'userID': 2
        })
        with allure.step("Отправка PUT запроса"):
            response = requests.request('PUT', url, headers=headers, data=data)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка изменений в посте"):
            assert response.json() == {
                'id': 1,
                'title': 'My cool update',
                'body': 'My cool message update',
                'userID': 2
            }

    @allure.feature("PUT - /posts")
    @allure.story("Изменение несуществующего поста (невалидные 'id')")
    def test_update_not_exist_post(self, base_url):
        url = base_url + '/posts'
        with allure.step("Получение общего количества постов"):
            response = requests.request('GET', url)
            response = response.json()
            count_posts = len(response)
        url1 = base_url + f'/posts/{count_posts + 1}'
        url2 = base_url + f'/posts/0'
        url3 = base_url + f'/posts/-1'
        urls = [url1, url2, url3]
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = json.dumps({
            'title': 'My cool update',
            'body': 'My cool message update',
            'userID': 2
        })
        with allure.step("Отправка PUT запроса"):
            responses = []
            for url in urls:
                response = requests.request('PUT', url, headers=headers, data=data)
                responses.append(response)
        with allure.step("Проверка статус кода на значение 500"):
            for response in responses:
                assert response.status_code == 500

    @allure.feature("PUT - /posts")
    @allure.story("Изменение существующего поста без тела запроса")
    def test_update_without_body_post(self, base_url):
        url = base_url + '/posts/1'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        with allure.step("Отправка PUT запроса"):
            response = requests.request('PUT', url, headers=headers)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with (allure.step("Проверка изменений в посте")):
            assert response.json() == {
                'id': 1
            }

    @allure.feature("PUT - /posts")
    @allure.story("Изменение одной записи существующего поста")
    def test_update_one_entry_post(self, base_url):
        url = base_url + '/posts/100'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = json.dumps({
                'title': 'My cool title update'
        })
        with allure.step("Отправка PUT запроса"):
            response = requests.request('PUT', url, headers=headers, data=data)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with (allure.step("Проверка изменений в посте")):
            assert response.json() == {
                'id': 100,
                'title': 'My cool title update'
            }

    @allure.feature("DELETE - /posts")
    @allure.story("Удаление существующего поста")
    def test_delete_exist_post(self, base_url):
        post_id = 1
        url = base_url + f'/posts/{post_id}'
        with allure.step("Отправка DELETE запроса"):
            response = requests.request('DELETE', url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка удалённого поста"):
            assert response.json() == {}

    @allure.feature("DELETE - /posts")
    @allure.story("Удаление несуществующих постов (невалидные 'id')")
    def test_delete_not_exist_post(self, base_url):
        url = base_url + '/posts'
        with allure.step("Получение общего количества постов"):
            response = requests.request('GET', url)
            response = response.json()
            count_posts = len(response)
        url1 = base_url + f'/posts/{count_posts + 1}'
        url2 = base_url + f'/posts/0'
        url3 = base_url + f'/posts/-1'
        urls = [url1, url2, url3]
        with allure.step("Отправка DELETE запросов"):
            responses = []
            for url in urls:
                response = requests.request('DELETE', url)
                responses.append(response)
        with allure.step("Проверка статус кода отправленных запросов на значение 200"):
            for response in responses:
                assert response.status_code == 200

    @allure.feature("DELETE - /posts")
    @allure.story("Удаление удалённого поста")
    def test_delete_deleted_post(self, base_url):
        post_id = 1
        url = base_url + f'/posts/{post_id}'
        with allure.step("Отправка DELETE запроса"):
            response = requests.request('DELETE', url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка удалённого поста"):
            assert response.json() == {}
        with allure.step("Отправка повторного DELETE запроса"):
            response = requests.request('DELETE', url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200

    @allure.feature("DELETE - /posts")
    @allure.story("Удаление созданного поста")
    def test_delete_created_post(self, base_url):
        url = base_url + '/posts/'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        data = json.dumps({
            'title': 'My cool post for delete',
            'body': 'My cool message for delete',
            'userID': 1
        })
        with allure.step("Отправка POST запроса"):
            response = requests.request('POST', url, headers=headers, data=data)
        with allure.step("Проверка статус кода на значение 201"):
            assert response.status_code == 201
        response = response.json()
        with allure.step("Проверка 'id' созданного поста на значение 101"):
            assert response['id'] == 101
        url = base_url + f'/posts/{response['id']}'
        with allure.step("Отправка DELETE запроса"):
            response = requests.request('DELETE', url)
        with allure.step("Проверка статус кода на значение 200"):
            assert response.status_code == 200
        with allure.step("Проверка удалённого созданного поста"):
            assert response.json() == {}
        with allure.step("Отправка GET запроса"):
            response = requests.request("GET", url)
        with allure.step("Проверка статус кода на значение 404"):
            assert response.status_code == 404
