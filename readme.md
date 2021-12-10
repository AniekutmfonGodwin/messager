# websocket endpoint
    /ws/chat/{receiver_id}/?token=<auth_token>

## Step to run messenger app
#### create a virtual enviroment and install dependencies
    pip install -r requirements.txt

#### Run migrations
    python manage.py migrate



#### run development server
    python manage.py runserver

#### [postman collection](./django_messenger.postman_collection.json)