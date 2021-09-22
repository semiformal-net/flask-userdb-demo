# Thingy!!

This is a Flask webapp with basic user authentication. Users can sign up, log in and log out. Registration is stored in Google Cloud SQL.

## Authentication

The project expects two sensitive files with credentials that are not in this repo. You must create them both before continuing.

`.env.dev`:
```FLASK_APP=project/__init__.py
FLASK_DEBUG=1
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://<SQLUSERNAME>:<SQLPASSWORD>@sqlproxy:3306/<SQLDATABASE>
SQL_HOST=sqlproxy
SQL_PORT=3306
APP_FOLDER=/usr/src/app
GOOGLE_APPLICATION_CREDENTIALS=/usr/bin/sqlproxy/srvc.json
INSTANCE=<PROJECT_ID>:<REGION>:sqldemo
```

You should replace:

- `<SQLUSERNAME>` : Set when you create your Google Cloud SQL database (eg, demo) 
- `<SQLPASSWORD>` : Set when you create your Google Cloud SQL database (eg, secretpass1)
- `<SQLDATABASE>` : Set when you create your Google Cloud SQL database (eg, demo)
- `<PROJECT_ID>` : The Google cloud project containing your SQL instance (eg, myproject)
- `<REGION>` : The Google cloud region containing your SQL instance (eg, us-central1)

`.env.prod`:
```
FLASK_APP=project/__init__.py
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://<SQLUSERNAME>:<SQLPASSWORD>@sqlproxy:3306/<SQLDATABASE>
SQL_HOST=sqlproxy
SQL_PORT=3306
APP_FOLDER=/home/app/web
GOOGLE_APPLICATION_CREDENTIALS=/usr/bin/sqlproxy/srvc.json
INSTANCE=<PROJECT_ID>:<REGION>:sqldemo
```

You should replace:

- `<SQLUSERNAME>` : Set when you create your Google Cloud SQL database (eg, demo) 
- `<SQLPASSWORD>` : Set when you create your Google Cloud SQL database (eg, secretpass1)
- `<SQLDATABASE>` : Set when you create your Google Cloud SQL database (eg, demo)
- `<PROJECT_ID>` : The Google cloud project containing your SQL instance (eg, myproject)
- `<REGION>` : The Google cloud region containing your SQL instance (eg, us-central1)

## Run mode

To run in *development* mode with the flask server and debug enabled,

```
docker-compose up -d --build
docker-compose logs # note the listening url, eg 172.1.1.1:5000
```

To run in *production* mode with gunicorn behind nginx,

```
docker-compose up -f docker-compose.prod.yml -d --build
```

Then visit [localhost:1337](http://localhost:1337)

## Cloud SQL Setup

You need to make a service account in GCP with [sql priviledges](https://cloud.google.com/sql/docs/mysql/sql-proxy#permissions). Then put the service account in services/sqlproxy/srvc.json

```
export PROJECT_ID=$(gcloud config get-value project)
gcloud iam service-accounts keys create /tmp/sqldemosrvc.json --iam-account=sqldemosrvc@${PROJECT_ID}.iam.gserviceaccount.com
cp /tmp/sqldemosrvc.json services/sqlproxy/srvc.json
```
Next set up a SQL user in the GCP console. Add the credentials to the `DATABASE_URL` in `.env.dev`

Get the instance of the Cloud SQL and add it to `INSTANCE` in `.env.dev`

## Thanks

This project benefited greatly from two tutorials: [one on flask and gunicorn](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/) from Michael Herman and [another on flask authentication](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login) from Anthony Herbert at digitalocean.

# GCP deployment

You can deploy the individual services as google app engine services. if you put the following,

`services/web/app.yaml`:

```
runtime: python39

service_account: <DATABASEUSER>@<PROJECT>.iam.gserviceaccount.com
service: diet-user-management
entrypoint: gunicorn project:app

env_variables:
 FLASK_APP: "project/__init__.py"
 FLASK_ENV: "production"
 DATABASE_URL: "mysql+pymysql://<DBUSER>:<DBPASS>@/<DB>?unix_socket=/cloudsql/<PROJECT>:us-central1:sqldemo"
 ```

You can then do `gcloud app deploy`
