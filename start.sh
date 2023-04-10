#!/bin/bash

cat /app/mailToTelegramForwarder.conf
/app/mailToTelegramForwarder.py --config /app/mailToTelegramForwarder.conf
