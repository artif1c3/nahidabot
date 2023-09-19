#!/bin/sh
export $(cat resources/secret.env | xargs)
python3 main.py