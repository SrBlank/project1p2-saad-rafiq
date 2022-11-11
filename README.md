# project1-saad-rafiq
[Click Here to Check Out the Website!](https://saadsmovies.fly.dev/)

## Software Stack
#### The website is composed of the following software:
#### Technologies 
- VSCode
- GitHub
- WSL
#### Frameworks
- Flask
- Fly
#### Libraries
- json
- os
- requests
- flask
- random
- dotenv
#### API
- TMDB API
- WikiMedia API

## Installation
### Preparing enviornment 
Begin by cloning the repository in WSL. Then start a virtual environment by running the following commands: 

```bash
cd ./project1-saad-rafiq/
python3 -m venv venv
```

Then activate the environment by running:

```bash
. venv/bin/activate
```

Once the virtual environment is activated run the following command to satisfy necessary dependencies:

```bash
python -m pip install -r requirements.txt
```

### Edit API Key
Now that our enviornment is setup create an account for [TMDB](https://www.themoviedb.org/?language=en-US) and follow the instructions on their [API documenation](https://developers.themoviedb.org/3/getting-started/introduction) page to be issued an API Key. We will use the v3 API key to request movie information.

Next create a file in the home directory of the cloned repo called `.env` and add the following line:

```
TMDB_API_KEY={KEY}
```

Replace the `{KEY}` with your API key. Fortunately, the WikiMedia API does not require to create an account or request a key so there will be no modification necessary for that.

### Deploying to Fly
Naviate to [fly.io](https://fly.io/) and create an account. Then in WSL run the following commands:

```bash
curl -L https://fly.io/install.sh | sh
flyctl auth login
```

Note: You may need to export to Fly to path after running the `curl` command

Once logged into fly on WSL run `flyctl launch`. When prompted for a name that will be name of your website. After the questions `Procfile` and `fly.toml` will be created. Edit `Procfile` to say the following:

```
# Modify this Procfile to fit your needs
web: gunicorn web_server:app
```
Then we are ready to deploy by running the following command.

```
flyctl deploy
```

We can then check status by doing `flyctl status` which should look something like this:

```
App
  Name     = saadsmovies
  Owner    = personal
  Version  = 1
  Status   = running
  Hostname = saadsmovies.fly.dev
  Platform = nomad

Deployment Status
  ID          = a283e4c6-f656-a445-f103-8f88fcd6187b
  Version     = v1
  Status      = successful
  Description = Deployment completed successfully
  Instances   = 1 desired, 1 placed, 1 healthy, 0 unhealthy
...
```
We are concerned with the `Hostname` which is the link to the website that is now deployed, [saadsmovies.fly.dev](https://saadsmovies.fly.dev/). We are also considered with `Status` and `Description` which should say successful.

## Challenges and Problems
### Technical Challenges
1. A technical challenge I came across was the WikiMedia API. The API documenation I felt was difficult to understand but once implemented I realized that a search more than likely results in multiple Wikipedia articles. To overcome this I used a `for loop` to iterate through the recieved array searching for the word `film`. In the case that it can not find it it will default to the first index of the array. This isn't a perfect solution however, I feel that this solution gets the job done efficently and works for the movies I have hardcoded in. 
2. The second challenge I came across was deploying to fly. I wanted to update my code so I can use the `tile.png` image however fly would not let me deploy. It kept on getting stuck on `Building Image` and would sit there forever. I restarted WSL, my computer, reinsntalled fly, tried a hardwired connection, and a bunch of other random poossible solutions. I finally ended up finding `flyctl doctor` which checked if everything was working as it should and found that my `agent` and `wireguard` had to be reset. 
### Known Problems
1. There are no default values so in the case where a Wiki article doesnt exist (which I did find) my array would fall out of index. 
2. I think my HTML and CSS could have been better. I believe it does not transfer to monitors that are not 1920x1080 very well and the formatting in general could have just been better. I found HTML and CSS very difficult to work with especically regarding alignment. 