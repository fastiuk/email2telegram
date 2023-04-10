#!/bin/bash

j2 mailToTelegramForwarder.conf.j2 > mailToTelegramForwarder.conf
cat /app/mailToTelegramForwarder.conf
/app/mailToTelegramForwarder.py --config /app/mailToTelegramForwarder.conf
