# VLOG - VRI Log - Verkeersregelinstallatie Log
An app to store the VRI logs.

## Summary
The ESB sents files to the POST endpoint provided by this app. This app loops over the file and stores every line 
in a separate database record. 


## To be decided:
POST /vri/101

format:
date, type, data

plain text:
2020-01-23 00:00:00.399,6,0600A10500
2020-01-23 00:00:02.220,10,0A0171010063
2020-01-23 00:00:02.941,10,0A0171010064

