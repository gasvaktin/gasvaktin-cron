#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import os

import git

import updater_utils

CONFIG = updater_utils.load_config('gasvaktin.config')

COMPANY_NAMES = {
	'ao': 'Atlantsolía',
	'dn': 'Dælan',
	'n1': 'N1',
	'ob': 'ÓB',
	'ol': 'Olís',
	'or': 'Orkan',
	'ox': 'Orkan X',
	'sk': 'Skeljungur'
}

def tweet_about_trends_changes():
	trends_file = os.path.join(
		CONFIG.get('Gasvaktin', 'repo'),
		'vaktin',
		'trends.min.json'
	)
	trends_data = None
	with open(trends_file, 'rb') as data_file:
		trends_data = json.load(data_file)
	# @timestamp_ten_minutes_ago below is bit of an ugly hack, this breaks if
	# something causes things to take more than 10 minutes to finish running,
	# usually things just take a couple of seconds so it's fine for now ..
	timestamp_ten_minutes_ago = (
		datetime.datetime.now() - datetime.timedelta(minutes=10)
	).isoformat()[:16]
	company_keys = trends_data.keys()
	company_keys.sort()
	tweet_msg = None
	for company_key in company_keys:
		bensin_diff = None
		b_last_price = None
		b_before_price = None
		diesel_diff = None
		d_last_price = None
		d_before_price = None
		last_change = trends_data[company_key][-1]
		if timestamp_ten_minutes_ago < last_change['timestamp']:
			before_change = trends_data[company_key][-2]
			# check bensin
			if last_change['mean_bensin95'] != before_change['mean_bensin95']:
				b_last_price = last_change['mean_bensin95']
				b_before_price = before_change['mean_bensin95']
				bensin_diff = round(b_last_price - b_before_price, 1)
			# check diesel
			if last_change['mean_diesel'] != before_change['mean_diesel']:
				d_last_price = last_change['mean_diesel']
				d_before_price = before_change['mean_diesel']
				diesel_diff = round(d_last_price - d_before_price, 1)
		if bensin_diff is not None and diesel_diff is not None:
			if bensin_diff == diesel_diff:
				tweet_msg = (
					'{company_name},'
					' bensin/diesel, {diff} ISK,'
					' {b_before_price} ➡ {b_last_price},'
					' {d_before_price} ➡ {d_last_price}\n'
					'#gasvaktin \n'
					'gasvaktin.is/trends/'
				).format(
					company_name=COMPANY_NAMES[company_key],
					diff=bensin_diff,
					b_before_price=b_before_price,
					b_last_price=b_last_price,
					d_before_price=d_before_price,
					d_last_price=d_last_price
				)
				break
			else:
				tweet_msg = (
					'{company_name},'
					' bensin, {bensin_diff} ISK,'
					' {b_before_price} ➡ {b_last_price},'
					' diesel, {diesel_diff} ISK,'
					' {d_before_price} ➡ {d_last_price}\n'
					'#gasvaktin \n'
					'gasvaktin.is/trends/'
				).format(
					company_name=COMPANY_NAMES[company_key],
					bensin_diff=bensin_diff,
					diesel_diff=diesel_diff,
					b_before_price=b_before_price,
					b_last_price=b_last_price,
					d_before_price=d_before_price,
					d_last_price=d_last_price
				)
				break
		elif bensin_diff is not None:
			tweet_msg = (
				'{company_name},'
				' bensin, {diff} ISK,'
				' {before_price} ➡ {last_price}\n'
				'#gasvaktin \n'
				'gasvaktin.is/trends/'
			).format(
				company_name=COMPANY_NAMES[company_key],
				diff=bensin_diff,
				before_price=b_before_price,
				last_price=b_last_price
			)
			break
		elif diesel_diff is not None:
			tweet_msg = (
				'{company_name},'
				' bensin, {diff} ISK,'
				' {before_price} ➡ {last_price}\n'
				'#gasvaktin \n'
				'gasvaktin.is/trends/?petrol=diesel'
			).format(
				company_name=COMPANY_NAMES[company_key],
				diff=diesel_diff,
				before_price=d_before_price,
				last_price=d_last_price
			)
			break
	if tweet_msg is not None:
		tweet_status = updater_utils.post_tweet(
			tweet_msg,
			CONFIG.get('TwitterAccess', 'consumer_key'),
			CONFIG.get('TwitterAccess', 'consumer_secret'),
			CONFIG.get('TwitterAccess', 'access_token_key'),
			CONFIG.get('TwitterAccess', 'access_token_secret')
		)
		tweet_notification_msg = (  # notify tweet url on slack
			'Trends change tweeted, see:\n'
			'https://twitter.com/gasvaktin/status/{tweet_id}'
		).format(tweet_id=tweet_status.id)
		updater_utils.slack_msg(
			tweet_notification_msg,
			CONFIG.get('Slackbot', 'token'),
			CONFIG.get('Slackbot', 'default_channel')
		)

def main():
	timestamp = datetime.datetime.now().isoformat()
	print 'Timestamp: %s' % (timestamp, )
	try:
		repo = git.Repo(CONFIG.get('Gasvaktin', 'repo'))
		print 'Pulling repo ..'
		print repo.git.pull()
		if repo.is_dirty():
			print 'Trends changes detected, commiting and pushing ..'
			commit_minified_msg = 'auto.trends.update.min.%s' % (timestamp, )
			commit_pretty_msg = 'auto.trends.update.%s' % (timestamp, )
			repo.git.commit('vaktin/trends.min.json', m=commit_minified_msg)
			repo.git.commit('vaktin/trends.json', m=commit_pretty_msg)
			repo.git.push()
			updater_utils.slack_msg(
				'Gasvaktin trends updated, %s' % (commit_pretty_msg, ),
				CONFIG.get('Slackbot', 'token'),
				CONFIG.get('Slackbot', 'default_channel')
			)
			print 'Done pushing, now tweeting ...'
			tweet_about_trends_changes()
			print 'Done, exiting ...'
		else:
			print 'No trends changes detected, exiting ...'
	except Exception as err:
		failure_msg = 'auto.trends.update failed (%s)' % (timestamp, )
		updater_utils.slack_msg(
			failure_msg,
			CONFIG.get('Slackbot', 'token'),
			CONFIG.get('Slackbot', 'default_channel')
		)
		raise err

if __name__ == '__main__':
	main()
