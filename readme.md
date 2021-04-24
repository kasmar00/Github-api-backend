# Github api client (backend)

Server side Github api client.

In this file `$` symbolizes that the following code is to be run in Linux (Bourne like) shell (ex. `Bash`,`Zsh`) as normal user. Example: `$ make` symbolizes that the user shall ran the `make` command in main folder of the project.

## Running

To run the application you should be using a fairly recent Linux distribution (tested under `Ubuntu 20.04.2` with Linux kernel `5.4.0`) with `python3` and `make` installed.

Running from provided makefile:

1. Create virtual environment: `$ make env`
2. Install necessary packages: `$ make install`
3. Run the application:
   - debug mode (files are reloaded on save): `$ make debug`
   - normal mode: `$ make run`
   - alternatively you can run it using the gunicorn server:
     1. activate the virtual environment: `$ source .env/bin/activate`
     2. run `gunicorn wsgi:app`

Regardless of run method, in command prompt server address should appear (ex. `127.0.0.1:5000`). Use it to access the app, as a replacement of `localhost` in examples below.

If you are running Windows you have to find your own versions of commands located in `makefile`, but the overall steps should be similar.

## Supported queries:

- `list`:
  Returns a json list of user's repositories, containing name and number of stars. Only public repositories are listed.

  Required parameter: `user` - username (github handle) of user, for which the list is to be fetched

  Example usage:

  `wget localhost/list?user=allegro`

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

  `$ wget localhost/?stars=allegro`

  Result:

  ```
  6368
  ```
