#!/bin/bash
# this script is used to boot a Docker container
for run in {1..5}; do
	flask db upgrade
	if [[ "$?" == "0" ]]; then
		break
	fi
	echo Deploy command failed, retrying in 5 secs...
	sleep 5
done
exec gunicorn -b 0.0.0.0:8080 --access-logfile - --error-logfile - study:app
