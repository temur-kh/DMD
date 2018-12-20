#!/usr/bin/env bash

cat dump.sql | docker exec -i mysql_container_name /usr/bin/mysql -u root --password=test company
