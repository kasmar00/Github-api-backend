# Github api client (backend)

Server side Github api client (task number 3) created during recruitment for Allegro Summer e-Xperience.

Author: Marcin Kasznia (https://github.com/kasmar00)

An example is deployed to heroku: https://github-backend-api-allegro.herokuapp.com/

In this file `$` symbolizes that the following code is to be run in Linux (Bourne like) shell (ex. `Bash`,`Zsh`) as normal user. Example: `$ make` symbolizes that the user shall ran the `make` command in main folder of the project.

## Running

To run the application you should be using a fairly recent Linux distribution (tested under `Ubuntu 20.04.2` with Linux kernel `5.4.0`) with `python3` and `make` installed.

If you are running Windows you have to find your own versions of commands located in `makefile`, but the overall steps, described below should be similar.

Instructions to run using docker (from provided `Dockerfile`) are also given below.

### On Linux

Running from provided makefile (all targets are described in `$ make help`):

1. Create virtual environment: `$ make env`
2. Install necessary packages: `$ make install`
3. Run the application:
   - debug mode (files are reloaded on save): `$ make debug`
   - normal mode: `$ make run`
   - alternatively you can run it using the gunicorn server (similar to heroku deployment):
     1. activate the virtual environment: `$ source .env/bin/activate`
     2. run `gunicorn wsgi:app`

Regardless of run method, application should print server address (ex. `127.0.0.1:5000`). Use it to access the app, as a replacement of `localhost` in examples below.

If you are using linux, but can't use `make` you should execute the commands located in makefile under targets: `env`, `install`, `run`/`debug`. Keep in mind that after creating virtual environment you should activate it `$ source .env/bin activate` and execute all the following commands from it.

### Authentication

Github api has a limit of 60 requests per hour for not authenticated users and 5000 for authenticated.

Application uses two environment variables to authenticate when using github api: `gh_user` (storing the github username) and `gh_token` (storing the personal access token). Both variables should be exported in shell in which app is being run (for example by calling `$ export gh_user=foo`).

Personal access tokens may be created in User settings -> Developer settings -> Personal access tokens (https://github.com/settings/tokens). It's enough to set access to `public_repo`.

### Using Docker

In following commands substitute the `python-docker` with your desired image name.

1. Build the provided `Dockerfile`: `$ docker build --tag python-docker .`
2. Authentication run
3. Export the environment variables `gh_user` and `gh_token`
4. Run the image: `$ docker run --env gh_user --env gh_token --publish 5000:5000 python-docker`
5. App should start at port `5000` on localhost

## Development

Project structure:

- `app/` - app source code
- `test/` - unit tests, and sample data json (for testing)
- `.github/workflows/test.yml` - workflow to run unit tests on commit and PR to `master` branch
- `wsgi.py` - entry point to application
- `makefile` - recipes to run app
- `Procfile` - deployment specs for heroku
- `requirements.txt` - python dependencies

### Testing

A few unit tests have been created and supplied with the app. To run the test use `$ make check`.

Tests are automatically run on commit and pull request to `master` branch.

Some tests rely on specific repositories on specific accounts. For example: repository `linux` being on `torvalds` account.

## Supported queries

- `list`:
  Returns a json list of user's repositories, containing name and number of stars. Only public repositories are listed.

  Required parameter: `user` - username (github handle) of user, for which the list is to be fetched

  Example usage:

  `$ curl localhost/list?user=allegro`

  or visit https://github-backend-api-allegro.herokuapp.com/list?user=allegro

  Result (head):

  ```
  [
    {
        "name": "akubra",
        "stars": 79
    },
    {
        "name": "allegro-api",
        "stars": 132
    },
    {
        "name": "allegro-tech-labs-iot",
        "stars": 1
    },
    (...)
  ]
  ```

- `stars`:
  returns a sum of all stars in user's repositories. Only public repositories are counted.

  Required parameter: `user` - username (github handle) of user, for which stars will be counted

  Example usage:

  `$ curl localhost/?stars=allegro`

  or visit https://github-backend-api-allegro.herokuapp.com/stars?user=allegro

  Result:

  ```
  6368
  ```

### HTTP response codes

Issuing `get` methods on above routes will return data and proper http response code. Possible response codes are:

- `200` - Everything went ok, data is returned
- `204` - User was not found (github api returned `404` code), empty data is returned
- `400` - Bad username was given, application will not process the query
- `504` - Github api is unavailable to application server. This may be due to github being down or server having no access to internet.
