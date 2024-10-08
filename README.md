# Coastal Erosion User Management Backend
A django server to manage user registration and login sequences.

## Library Installation
#### 1. Create a virtual environment
 ```py -m venv .venv```
#### 2. Activate the virtual environment
 ```.venv\scripts\activate```
#### 3. Install django
```py -m pip install django```
#### 4. Install all other libraries
```
    py -m pip install djangorestframework django-cors-headers
    py -m pip install djangorestframework-simplejwt
    py -m pip install Django-Verify-Email
    py -m pip install six
```
#### 5. Create a folder to hold the project in the same directory as the virtual environment created

#### 6. Navigate into the folder created and clone the repository
``` cd folderName```
#### 7. Run the server
``` py manage.py runsever ```
 If successful then the output should look like this
``` Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
October 27, 2022 - 13:03:14
Django version 4.1.2, using settings 'coastal_erosion.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Authentication
Using ```axios``` you can send a request and then get a response which is a dictionary with a response message and boolean to show whether login or registration was successful. 

### Login sequence
* Make a **POST** request to SERVER_URL/api/login/. The payload should be in this format:
```
{
    "email": "example@example.com",
    "password": "password",
}
```
Remember to pass ```withCredentials=true``` when sending the login request. This will send a httponly cookie that the server will use to automatically authenticate the user.

If the operation is successful, this is the response you'll get.

```
    {
        'email':email,
        'user_metadata':{
            'firstName':first_name,
            'lastName':last_name,
            'institution':institution,
            'sector':sector,
            'role':role,
            'country':country 
        } 
    }
```

The access token is automatically set and stored by the browser such that it is inaccessible from the frontend. This helps prevent malicious `Cross Site Scripting (XSS)` and `Cross Site Request Forgery (CSRF)` attacks. Any other request that requires authentication will have to include ```withCredentials=true``` in the request so that the token is included in the request.
    
### Sign-up/Registration Sequence with axios
* Make a **POST** request to SERVER_URL/api/signup/. The payload should be in this format:

```
{
    "first_name":"firstname",
    "last_name":"lastname",
    "email": "example@example.com",
    "institution": "institution",
    "sector": "sector",
    "role": "role",
    "other_role": "other_role", // optional
    "country": "country",
    "password": "password",
}
```

### Get user details
* Make a **GET** request to SERVER_URL/api/getuser/. The user has to be authenticated so make sure to pass ```withCredentials=True``` in the request, otherwise the operation will be forbidden.

If the operation is successful, this is the response you'll get.

```
    {
        'email':email,
        'user_metadata':{
            'firstName':first_name,
            'lastName':last_name,
            'institution':institution,
            'sector':sector,
            'role':role,
            'country':country 
        } 
    }
```

### Logout sequence
* Make a **GET** request to SERVER_URL/api/logout/. The user has to be authenticated so make sure to pass ```withCredentials=True``` in the request, otherwise the operation will be forbidden. This will delete the access token and logout the user.

### Request password change
* Make a **POST** request to SERVER_URL/api/passwordupdate/. The payload should be in this format:

```
    {
        "email":"example@example.com"
    }
```
 A verification email will be sent to the provided email which will redirect the user to a page to provide a new password.

### Change password
* Make a **POST** request to SERVER_URL/api/resetpassword/. The payload should be in this format:
```
    {
        'token':'token',
        'uid':'uid',
        'password':'password'
    }
```
**NB:** Obtain the `token` and `uid` from the password reset page url. It should look like this:
`SERVER_URL/#/update-password?access_token={token}&uid={uid}`















