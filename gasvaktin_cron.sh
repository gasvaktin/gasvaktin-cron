# gasvaktin absolute path (UPDATE PATH)
gasvaktin_repo_path=/path/to/repo/gasvaktin
# gasvaktin-cron absolute path (UPDATE PATH)
gasvaktin_cron_repo_path=/path/to/repo/gasvaktin-cron
# our lovely python (UPDATE PATH)
python=/usr/bin/python

# create timestamp
MY_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

cd ${gasvaktin_repo_path}/scripts
${python} pricer.py
cd ${gasvaktin_cron_repo_path}
${python} gasvaktin_updater.py  > logs/run_${MY_TIMESTAMP}.log 2>&1
