# gasvaktin-cron
Automation scripts run as cronjobs to update [gasvaktin](https://github.com/gasvaktin/gasvaktin) price information.

PLEASE DO NOT INSTALL THIS CRONTAB. YOU DO NOT NEED TO DO SO AS LONG AS GASVAKTIN IS RUNNING IT. THIS REPOSITORY EXISTS ONLY TO KEEP A BACKUP OF THE CRONTAB SETUP IN CASE BAD THINGS HAPPEN, AND OF COURSE EXPOSES IT TO THOSE CURIOUS ABOUT IT.

## Setup

Few things need to be done.

You'll need to have done "Setup and usage" in [gasvaktin](https://github.com/gasvaktin/gasvaktin).

Install the required python modules

	pip install -r pip_requirements.txt

Copy the example config

	cp gasvaktin.example.config gasvaktin.config

and populate the config file with correct values.

Open `crontab.txt` and fill in correct absolute path to the repository folder.

Open `gasvaktin_cron.sh` and fill in correct paths to corresponding repositories.

Run the following

	mkdir logs
	crontab -l > tempcronfile.txt
	cat crontab.txt >> tempcronfile.txt
	crontab tempcronfile.txt
	rm tempcronfile.txt

and you're done.

If you ever need to change the crontab simply do so with `crontab -e`.

PLEASE DO NOT INSTALL THIS CRONTAB. YOU DO NOT NEED TO DO SO AS LONG AS GASVAKTIN IS RUNNING IT. THIS REPOSITORY EXISTS ONLY TO KEEP A BACKUP OF THE CRONTAB SETUP IN CASE BAD THINGS HAPPEN, AND OF COURSE EXPOSES IT TO THOSE CURIOUS ABOUT IT.
