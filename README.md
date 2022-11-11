# project1-saad-rafiq
[Click Here to Check Out the Website!](https://movieprojsaad.fly.dev/)

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

### Edit Database URI
Create a postgres cluster following the directions on this [github repo](https://github.com/laithhas/ip-milestone-2-demo). In the process of creation you will get a Database URI link. Save this link and put in your `.env` like so:

```
DATABASE_URL=
```

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
  Name     = movieprojsaad
  Owner    = personal
  Version  = 1
  Status   = running
  Hostname = movieprojsaad.fly.dev
  Platform = nomad

Deployment Status
  ID          = a283e4c6-f656-a445-f103-8f88fcd6187b
  Version     = v1
  Status      = successful
  Description = Deployment completed successfully
  Instances   = 1 desired, 1 placed, 1 healthy, 0 unhealthy
...
```
We are concerned with the `Hostname` which is the link to the website that is now deployed, [saadsmovies.fly.dev](https://movieprojsaad.fly.dev/). We are also considered with `Status` and `Description` which should say successful.

## Challenges and Problems
### Implementaion Issues
1. I had trouble implementing a lot of the HTML ideas I had. I found HTML and CSS challenging to work with as it seemed like there are 10 different ways to approach the same problem. Becuase of this issue I sat down one day and really tried to figure things out and I came up with a methadology to coding in html. The methadology was to have `div` container then another `div` for the contents. This allowed me to seperate my code into header, footer, body, and image containers making formatting a lot easier.
2. The second implementation issue I had was how URL scheming was going to be. I feel like most websites I go to have a URL scheme that makes sense however I was uncertain on if and how to organize. I ended up settling for a scheme that makes sense to me as when a user is in `/movie` and submits a review the submission is `/movie/handle_submission`.
### Technical Issues
1. A technical issue I had was connecting the database locally then later on fly. This was a huge issue for me as I was not able to make a lot of progress without the database. Therefore I spent most of my time working on the database and issues I had with it. The biggest issue I had was finding the right database URI since for some reason fly would give me several URIs and I was not sure which to use. I ended up finally setting the right secrets and the variables to get my database to work.
2. The second issue I had was using flask_login. I felt that documentation wasnt the greatest and there was a lot going on as far as user authentication and logging in/out goes. I am specifically talking about the `.is_authenticated` function as I didnt quite understand how to use it. After looking at enough examples however I got the correct implementation of the library. 


##
NOTE: MY COMMITS ARE ALL ON project1-saad-rafiq REPOSITORY AS I WAS NOT CERTAIN ABOUT IF WE NEEDED TO USE THE SAME URL FOR THE PROJECT OR NOT. PLEASE VIST THIS LINK TO VIEW MY COMMIT HISTORY https://github.com/SrBlank/project1-saad-rafiq