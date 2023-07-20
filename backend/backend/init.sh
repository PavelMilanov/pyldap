#!/bin/sh

flag=$1

case "$flag" in
    server)
        uvicorn server:app --host 0.0.0.0 --port 8000;;

    background)
        dramatiq background_tasks;;
esac
