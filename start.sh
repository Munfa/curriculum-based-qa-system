#!/bin/bash
fallocate -l 2G /tmp/swapfile
chmod 600 /tmp/swapfile
mkswap /tmp/swapfile
swapon /tmp/swapfile

uvicorn api:app --host 0.0.0.0 --port $PORT