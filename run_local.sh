#!/bin/bash
set -o allexport; 
source .env;
set +o allexport;
uvicorn server:app;