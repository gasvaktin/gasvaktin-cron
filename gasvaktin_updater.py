#!/usr/bin/python
# -*- coding: utf-8 -*--
import datetime

import git

import updater_utils

CONFIG = updater_utils.load_config('gasvaktin.config')

def main():
	timestamp = datetime.datetime.now().isoformat()
	print 'Timestamp: %s' % (timestamp, )
	try:
		repo = git.Repo(CONFIG.get('Gasvaktin', 'repo'))
		print 'Pulling repo ..'
		print repo.git.pull()
		if repo.is_dirty():
			print 'Changes detected, commiting and pushing ..'
			commit_minified_msg = 'auto.prices.update.min.%s' % (timestamp, )
			commit_pretty_msg = 'auto.prices.update.%s' % (timestamp, )
			repo.git.commit('vaktin/gas.min.json', m=commit_minified_msg)
			repo.git.commit('vaktin/gas.json', m=commit_pretty_msg)
			repo.git.push()
			updater_utils.slack_msg(
				'Gasvaktin changes available, %s' % (commit_pretty_msg, ),
				CONFIG.get('Slackbot', 'token'),
				CONFIG.get('Slackbot', 'default_channel')
			)
			updater_utils.update_gist_timestamp(
				timestamp,
				CONFIG.get('GistAccess', 'username'),
				CONFIG.get('GistAccess', 'api_token'),
				CONFIG.get('GistFiles', 'prices_changed_timestamp')
			)
			print 'Done, exiting ...'
		else:
			print 'No changes detected, exiting ...'
		updater_utils.update_gist_timestamp(
			timestamp,
			CONFIG.get('GistAccess', 'username'),
			CONFIG.get('GistAccess', 'api_token'),
			CONFIG.get('GistFiles', 'prices_lookup_timestamp')
		)
	except Exception as err:
		failure_msg = 'auto.prices.update failed (%s)' % (timestamp, )
		updater_utils.slack_msg(
			failure_msg,
			CONFIG.get('Slackbot', 'token'),
			CONFIG.get('Slackbot', 'default_channel')
		)
		raise err

if __name__ == '__main__':
	main()
