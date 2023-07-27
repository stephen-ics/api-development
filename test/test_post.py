from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    with authorized_client:
        res = authorized_client.get('/posts/')

        def validate(post):
            return schemas.PostResponse(**post)
        
        posts_map = map(validate, res.json())
        posts = list(posts_map)

        assert len(res.json()) == len(test_posts)
        assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    with client:
        res = client.get('/posts/')
        assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    with client:
        res = client.get(f'/posts/{test_posts[0].id}')
        assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    with authorized_client:
        res = authorized_client.get('/posts/8888')
        assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    with authorized_client:
        res = authorized_client.get(f'/posts/{test_posts[0].id}')

        post = schemas.PostResponse(**res.json())
        
        assert post.Post.id == test_posts[0].id
        assert post.Post.title == test_posts[0].title
        assert post.Post.content == test_posts[0].content

        assert res.status_code == 200

@pytest.mark.parametrize('title, content, published', [
    ('cool title', 'cool content', True),
    ('favourite pizza', 'i love cheese pizza', False),
    ('tallest skyscraper', 'Wooo', True)
])
def test_create_post(authorized_client, test_posts, test_user, title, content, published):
    with authorized_client:
        res = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})
        response = res.json()
        print(response)

        created_post = schemas.PostResponseBase(**res.json())

        assert created_post.title == title
        assert created_post.content == content
        assert created_post.published == published
        assert created_post.user_id == test_user['id']
        assert res.status_code == 201

def test_create_post_default_published_true(authorized_client, test_posts, test_user):
    with authorized_client:
        res = authorized_client.post('/posts/', json={'title': 'cool title', 'content': 'cool content'})

        created_post = schemas.PostResponseBase(**res.json())

        assert created_post.title == 'cool title'
        assert created_post.content == 'cool content'
        assert created_post.published == True
        assert created_post.user_id == test_user['id']
        assert res.status_code == 201   

def test_unauthorized_user_create_post(client, test_posts, test_user):
    with client: 
        res = client.post('/posts/', json={'title': 'cool title', 'content': 'cool content'})
        
        assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts, test_user):
    with client:
        res = client.delete(f'/posts/{test_posts[0].id}')

        assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts, test_user):
    with authorized_client:
        res = authorized_client.delete(f'/posts/{test_posts[0].id}')

        assert res.status_code == 204     

def test_delete_post_non_exist(authorized_client, test_posts, test_user):
    with authorized_client:
        res = authorized_client.delete('/posts/800000')

        assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    with authorized_client:
        res = authorized_client.delete(f'/posts/{test_posts[3].id}')

        assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    with authorized_client:
        data = {
            'title': 'updated title',
            'content': 'updated content',
            'published': 'True',
            "id": test_posts[0].id
        }

        res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
        updated_post = schemas.PostResponseBase(**res.json())

        assert updated_post.title == data['title']
        assert updated_post.content == data['content']
        assert res.status_code == 200

def test_update_other_user_post(authorized_client, test_posts, test_user, test_user2):
    with authorized_client:
        data = {
            'title': 'updated title',
            'content': 'updated content',
            'published': 'True',
            'id': test_posts[3].id
        } 
        
        res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)

        assert res.status_code == 403
        
def test_unauthorized_user_update_post(client, test_posts, test_user):
    with client:
        data = {
            'title': 'updated title',
            'content': 'updated content',
            'published': 'True',
            'id': test_posts[3].id
        } 

        res = client.put(f'/posts/{test_posts[0].id}', json=data)

        assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts, test_user):    
    with authorized_client:
        data = {
            'title': 'updated title',
            'content': 'updated content',
            'published': 'True',
            'id': test_posts[3].id
        } 

        res = authorized_client.put('/posts/800000', json=data)

        assert res.status_code == 404