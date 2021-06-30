# Conda Metrics🐍

 Goal is to gather Conda metrics in order to parse and display a helpful dashboard

 Full tech spec is  [here](https://docs.google.com/document/d/1wpjfUZ2NT89BQuGzEFBlZ6IF_LgNnTCLkboaBLcpVFY/edit#heading=h.vv37mdxyde7)

 This was made using the excellant [django-vue-template](https://github.com/gtalarico/django-vue-template)

 # Dev Info

Vue and Django are clearly separated in this project. Vue, Yarn and Webpack handles all frontend logic and bundling assessments. Django and Django REST framework to manage Data Models, Web API and serve static files.

While it's possible to add endpoints to serve django-rendered html responses, the intention is to use Django primarily for the backend, and have view rendering and routing and handled by Vue + Vue Router as a Single Page Application (SPA).

Out of the box, Django will serve the application entry point (`index.html` + bundled assets) at `/` ,
data at `/api/`, and static files at `/static/`. Django admin panel is also available at `/admin/` and can be extended as needed.

The application templates from Vue CLI `create` and Django `createproject` are kept as close as possible to their
original state, except where a different configuration is needed for better integration of the two frameworks.

### Includes

* Django
* Django REST framework
* Django Whitenoise, CDN Ready
* Vue CLI 3
* Vue Router
* Vuex
* Gunicorn
* Configuration for Heroku Deployment

### Template Structure


| Location             |  Content                                   |
|----------------------|--------------------------------------------|
| `/backend`           | Django Project & Backend Config            |
| `/backend/api`       | Django App (`/api`)                        |
| `/src`               | Vue App .                                  |
| `/src/main.js`       | JS Application Entry Point                 |
| `/public/index.html` | [Html Application Entry Point](https://cli.vuejs.org/guide/html-and-static-assets.html) (`/`)         |
| `/public/static`     | Static Assets                              |
| `/dist/`             | Bundled Assets Output (generated at `yarn build`) |

## Prerequisites

Before getting started you should have the following installed and running:

- [] Yarn - [instructions](https://yarnpkg.com/en/docs/install)
- [] Vue CLI 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [] Python 3 - [instructions](https://wiki.python.org/moin/BeginnersGuide)
- [] Pipenv - [instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Setup Template

```
$ git clone https://github.com/gtalarico/django-vue-template
$ cd django-vue-template
```

Setup

Note: Conda nor Conda Forge do not have gunicorn packages for Windows, sad day. If you are on Mac or Linux you can just update the reqs and skip the below pip install
```
$ yarn install
$ pip install gunicorn  
$ python manage.py migrate
```

## Running Development Servers

```
$ python manage.py runserver
```

From another tab in the same directory:

```
$ yarn serve
```

The Vue application will be served from [`localhost:8080`](http://localhost:8080/) and the Django API
and static files will be served from [`localhost:8000`](http://localhost:8000/).

The dual dev server setup allows you to take advantage of
webpack's development server with hot module replacement.
Proxy config in [`vue.config.js`](/vue.config.js) is used to route the requests
back to django's API on port 8000.

If you would rather run a single dev server, you can run Django's
development server only on `:8000`, and you have to build the Vue app first
and the page will not reload on changes.

```
$ yarn build
$ python manage.py runserver
```

## Deploy

* Set `ALLOWED_HOSTS` on [`backend.settings.prod`](/backend/settings/prod.py)

### Heroku Server
```
$ heroku apps:create django-vue-template-demo
$ heroku git:remote --app django-vue-template-demo
$ heroku buildpacks:add --index 1 heroku/nodejs
$ heroku buildpacks:add --index 2 heroku/python
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set DJANGO_SETTINGS_MODULE=backend.settings.prod
$ heroku config:set DJANGO_SECRET_KEY='...(your django SECRET_KEY value)...'

$ git push heroku
```

Heroku's nodejs buildpack will handle install for all the dependencies from the [`package.json`](/package.json) file.
It will then trigger the `postinstall` command which calls `yarn build`.
This will create the bundled `dist` folder which will be served by whitenoise.

The python buildpack will detect the [`Pipfile`](/Pipfile) and install all the python dependencies.

The [`Procfile`](/Procfile) will run Django migrations and then launch Django'S app using gunicorn, as recommended by heroku.

##### Heroku One Click Deploy

## ###TODO// Update the heroky one click deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?xxxxxxxxxx)

## Static Assets

See `settings.dev` and [`vue.config.js`](/vue.config.js) for notes on static assets strategy.

This template implements the approach suggested by Whitenoise Django.
For more details see [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/django.html)

It uses Django Whitenoise to serve all static files and Vue bundled files at `/static/`.
While it might seem inefficient, the issue is immediately solved by adding a CDN
with Cloudfront or similar.
Use [`vue.config.js`](/vue.config.js) > `baseUrl` option to set point all your assets to the CDN,
and then set your CDN's origin back to your domains `/static` url.

Whitenoise will serve static files to your CDN once, but then those assets are cached
and served directly by the CDN.

This allows for an extremely simple setup without the need for a separate static server.

[Cloudfront Setup Wiki](https://github.com/gtalarico/django-vue-template/wiki/Setup-CDN-on-Cloud-Front)
