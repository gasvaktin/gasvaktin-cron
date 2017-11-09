# gasvaktin absolute path (UPDATE PATH)
gasvaktin_repo_path=/path/to/repo/gasvaktin
# gasvaktin-cron absolute path (UPDATE PATH)
gasvaktin_cron_repo_path=/path/to/repo/gasvaktin-cron
# our lovely python (UPDATE PATH)
python=/usr/bin/python

# create logging folder if needed
mkdir -p ${gasvaktin_cron_repo_path}/logs

# generate timestamp
MY_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# update prices
cd ${gasvaktin_repo_path}/scripts
${python} pricer.py || ${python} slack_msg.py "pricer failure: ${MY_TIMESTAMP}"
cd ${gasvaktin_cron_repo_path}
${python} gasvaktin_updater.py  > logs/run_${MY_TIMESTAMP}.log 2>&1

# update trends
cd ${gasvaktin_repo_path}/scripts
${python} trends.py || ${python} slack_msg.py "trends failure: ${MY_TIMESTAMP}"
cd ${gasvaktin_cron_repo_path}
${python} gasvaktin_trends_updater.py  > logs/run_${MY_TIMESTAMP}_trends.log 2>&1

