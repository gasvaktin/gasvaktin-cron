#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import datetime

import git
import simplegist
import slackclient

CONFIG = ConfigParser.RawConfigParser()
CONFIG.read('gasvaktin.config')

def slack_msg(message, channel=CONFIG.get('Slackbot', 'default_channel')):
	'''
	send message to slack
	'''
	sc = slackclient.SlackClient(CONFIG.get('Slackbot', 'token'))
	if sc.rtm_connect():
		sc.rtm_send_message(channel, message)
	else:
		print 'slack_msg() failed, invalid token? or no network access?'

def update_gist_timestamp(gist_id, timestamp):
	'''
	update timestamp gist
	'''
	ghGist = simplegist.Simplegist(
		username=CONFIG.get('GistAccess', 'username'),
		api_token=CONFIG.get('GistAccess', 'api_token')
	)
	ghGist.profile().edit(id=gist_id, content=timestamp)

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
			slack_msg('Gasvaktin changes available, %s' % (commit_pretty_msg, ))
			update_gist_timestamp(CONFIG.get('GistFiles', 'prices_changed_timestamp'), timestamp)
			print 'Done, exiting ...'
		else:
			print 'No changes detected, exiting ...'
		update_gist_timestamp(CONFIG.get('GistFiles', 'prices_lookup_timestamp'), timestamp)
	except Exception as err:
		failure_msg = 'auto.prices.update failed (%s)' % (timestamp, )
		slack_msg(failure_msg)
		raise err

if __name__ == '__main__':
	main()
