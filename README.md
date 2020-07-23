# Waarnemingen voertuigen

This project is part of the waarnemingen cluster.

## VLOG - VRI Log - Verkeersregelinstallatie Log
An app to store the VRI logs. The ESB sends files to the POST endpoint provided by this app. This app loops over the 
file and stores every line in a separate database record. 

## Reistijden
An app to store the reistijden of cars driving through Amsterdam. It's an endpoint to which XML files are posted.


### TimescaleDB
This code base uses the timescaledb postgres extension. On Debian based systems it can be installed using

    sudo add-apt-repository ppa:timescale/timescaledb-ppa
    sudo apt install timescaledb-postgresql-12
    yes | sudo timescaledb-tune
    sudo service postgresql restart

