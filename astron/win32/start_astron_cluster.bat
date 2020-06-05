@echo off
cd ../
title Astron
astrond --pretty --loglevel info config/astrond.yml
pause