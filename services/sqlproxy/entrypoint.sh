#!/bin/sh

/usr/bin/sqlproxy/cloud_sql_proxy.linux.amd64 -instances=${INSTANCE}=tcp:0.0.0.0:3306 -credential_file=${GOOGLE_APPLICATION_CREDENTIALS}

exec "$@"