#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser

import simplegist
import slackclient
import twitter

def load_config(config_name):
    '''
    load config
    '''
    config = ConfigParser.RawConfigParser()
    config.read(config_name)
    return config

def slack_msg(message, slack_token, channel):
    '''
    send message to slack
    '''
    sc = slackclient.SlackClient(slack_token)
    if sc.rtm_connect():
        sc.rtm_send_message(channel, message)
    else:
        print 'slack_msg() failed, invalid token? or no network access?'

def update_gist_timestamp(timestamp, username, api_token, gist_id):
    '''
    update timestamp gist
    '''
    gh_gist = simplegist.Simplegist(username=username, api_token=api_token)
    gh_gist.profile().edit(id=gist_id, content=timestamp)

def post_tweet(msg, c_key, c_secret, a_key, a_secret):
    '''
    tweet
    '''
    api = twitter.Api(
        consumer_key=c_key,
        consumer_secret=c_secret,
        access_token_key=a_key,
        access_token_secret=a_secret
    )
    return api.PostUpdate(msg)  # return tweet post status object
