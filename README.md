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
Django version 4.1.2, using settings 'my_tennis_club.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Front end implementation
Using ```axios``` you can send a request and then get a response which is a dictionary with a response message and boolean to show whether login or registration was successful.

### Login sequence using axios
```const handleSubmit = async (e) => {
        e.preventDefault();
        await axios.post(' http://127.0.0.1:8000/login/', {
            "email": logdata.email,
            "password": logdata.password
        }).then((res) => {
            var log = res.data;
            console.log(log);

            if (log.Success) {
                const accessToken = log.access_token// Your access token here
                const decodedToken = jwt_decode(accessToken);
                
                if (decodedToken) {
                    console.log(decodedToken)
                    const data={
                        email:decodedToken.email,
                        first_name:decodedToken.first_name,
                        last_name:decodedToken.last_name,
                        phone_number:decodedToken.phone_number,
                        gender:decodedToken.gender,
                        emergecy_contact:decodedToken.emergency_contact
                    }
                    todash(data); 
                } 
                //todash(log.first_name,log.last_name);
            } else {
                console.log(log.Message)
            }
        }).catch((err) => console.log(err))
    }
  ```
    
    
### Sign-up/Registration Sequence
```
const handleSubmit = async (e) => {
        e.preventDefault()
        //check password and confirm password front-end
        if(confirmPassword !== Password){
            setVal("Passwords do not match");
            setCol("rgb(153,15,2)");
        }else{
            await axios.post(' http://127.0.0.1:8000/signup/',{
                'first_name':logdata.first_name,
                'last_name':logdata.last_name,
                'email':logdata.email,
                'institution':logdata.phone_number,
                'password':logdata.password
            }).then((res)=>{
                if (res.data.Success){
                    navigate("/")
                }else{
                    console.log(res.data.Message)
                }    
            }).catch((err) => console.log(err))
        } 
    }
  ```






