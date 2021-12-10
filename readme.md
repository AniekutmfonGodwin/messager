# websocket endpoint
    /ws/chat/{receiver_id}/?token=<auth_token>

## websocket data schema
    {
        event:"NEW_MESSAGE"|"READ_MESSAGE",
        payload:Object
    }

    e.g
    socket.send({
        event:"NEW_MESSAGE",
        payload:{
            message:string
        }
    })

    socket.send({
        event:"READ_MESSAGE",
        payload:{
            message_id:number
        }
    })

### send and listen to new message e.g
    let url = "ws//example.com/ws/chat/{receiver_id}/?token=<auth_token>"
    let socket = new Websocket(url)

    socket.send({
        event:"NEW_MESSAGE",
        payload:{
            message:string
        }
    })

    socket.onmessage = function(event) {
        console.debug("new message", event);
    };

    


### send and listen to read message e.g
    let url = "ws//example.com/ws/chat/{receiver_id}/?token=<auth_token>"
    let socket = new Websocket(url)


    socket.send({
        event:"READ_MESSAGE",
        payload:{
            message_id:number
        }
    })

    socket.onmessage = function(event) {
        console.debug("read message:", event);
    };



## Step to run messenger app
#### create a virtual enviroment and install dependencies
    pip install -r requirements.txt

#### Run migrations
    python manage.py migrate



#### run development server
    python manage.py runserver

#### [postman collection](./django_messenger.postman_collection.json)