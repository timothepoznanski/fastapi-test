from fastapi import FastAPI

app = FastAPI()

data = {
    'users': [
        'Alice',
        'Bob',
        'Charlie',
        'David',
        'Eve',
        'Frank',
        'Grace']
}

@app.get("/users")
async def get_users():
    # return our data and 200 OK code
    return {'data': data}

@app.post("/users")
async def post_user(user: str):
    # if the user is already present, we do not add it to the data
    if user in data['users']:
        # so just return the response with a message saying it already exists
        return {'data': data, 'message': "the user already exists"}
    
    # however, if it is not present, we add the user to the data
    else:
        data['users'].append(user)
        # return response
        return {'data': data, 'message': "the user has been added"}

@app.delete("/user")
async def delete_user(user: str):
    # if the user is present, delete it
    if user in data['users']:
        data['users'].remove(user)
        # return response confirming deletion
        return {'data': data, 'message': 'the user has been deleted'}
    
    # if it is not present, just return the response
    else:
        return {'data': data, 'message': "the user does not exist"}

@app.put("/users")
async def put_user(old_user: str, new_user: str):
    # if the old user is present, update with the new user
    if old_user in data['users']:
        index = data['users'].index(old_user)
        data['users'][index] = new_user
        # return response confirming the update
        return {'data': data, 'message': "the user has been updated"}
    
    # if it is not present, just return the response
    else:
        return {'data': data, 'message': "the user does not exist"}

@app.delete("/users")
async def delete_all_users():
    # clear the list of users
    data['users'].clear()
    # return response confirming the deletion of all users
    return {'data': data, 'message': 'all users have been deleted'}

@app.get("/health")
async def health_check():
    # return a simple health check response
    return {'status': 'healthy'}

@app.get("/version")
async def get_version():
    # return the version of the application
    return {'version': '1.0.0'}

@app.get("/metrics")
async def get_metrics():
    # return some example metrics
    return {
        'total_users': len(data['users']),
        'example_metric': 12345
    }
