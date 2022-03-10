GitLab clone/pull all projects into their group/subgroup
-------------

This is a python script distributed in a docker image that will clone/pull all repos from a specific (root) Gitlab group maintaining their group/subgroup tree structure.

A sleep mechanism has been used to prevent resources exhaustion and machine brain froze in case you are dealing with hundreds of repos :)

Pre-requisites
--------------

This tool requires,
[Docker](https://docker.com/) and [Docker
Compose](https://docs.docker.com/compose/) 

Configuring
----------
Create a `.env` file using copy of `.env.sample`, provide your 
```
GITLAB_HOST=https://gitlab.com
GITLAB_TOKEN=glpat-XXXXXXXXXXXXXXXXXXX
GROUP_ID=1
```

Running
---------

`docker compose up`

If configuration is correct, your repos will start clone if not existing OR pull the latest changes if they already exist in your local machine.

This tool will keep alive the docker container for a minute to allow machine to properly sync the volumes between the host and the container.

When everything is completed a `"All done!"` message will be shown, and the container will exit.