<p align="center">
  <img src="./NEMESIS_TEAM_LOGO.jpg" alt="NEMESIS TEAM LOGO" style="border-radius:5px"/>
</p>

# InstaSucker
 Gets instagram public username and returns usefull informations like profilepic(b64), video_urls etc.

## Information
 - this project contains a main python file and the instagram-private-api module files,
 the main file uses the module only for authentication and the main program that extracts the data is our main.py file.
 * the instapi directory is needed and the instagram-private-api module must be installed before use.
---
## How to run
 * First of all run:
    ```
    pip install -r requirements.txt
    ```

 1- to run directly :
 * run the main.py file with or without arguments, if you do not provide the required information with arguments it will ask you to enter them manually in the terminal.
 * if you run the file directly the output will automatically be saved to an outputxx.json file where xx is a random number.
    
 2- to use this feature in another file : 
 * just import the extractIG function from main.py -> "`from main import extractIG`" 

  * you may face some import errors from 1 outta 10000 but if you did you have to manually put a . at the
  beggrning of some imports, I'll talk about it more at the end.

  * by importing and using "`extractIG`" in another file it will return all information as json.
  * to user the returned json for those who are not familiar just follow the steps below:
    * data = extractIG('username', 'password', 'target_username')
    * data = json.loads(data)

    now to access the data just follow the path like this:
    ```py
        data["user"]["username"]
    ````

    the returned json structure is:
    ```py
        allInfo = {
        'user': {
            'username' : '',
            'uid' : '',
            'bio' : '',
            'followings_count' : '',
            'followers_count' : '',
            'profile_pic_url' : '',
            'profile_pic_b64': '',
            'videos' : [],

            }
    }
    ```
    to access the videos loop through them:
    ```py
    videos = data["user"]["videos"]
    for video in videos:
        ... # do anything you want to each video
    ```
---
## NOTES
* Do not try to print the data because the returned image is formated to base64 and that's a lots of text and makes it unreadable when printed to the <strong>`terminal`.</strong>

* As I said at the beggining after running the main file directly all the returned data will be stored in a json file, you can use "`Beautify`" extension to make the json file more readable and tidier.

### Do not HeZiTaTe to open issues if there was a problem!
<p align="center">
❤️❤️❤️
</p>