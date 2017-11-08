#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse

import updater_utils

CONFIG = updater_utils.load_config('gasvaktin.config')


def main():
    parser = argparse.ArgumentParser()
    help_txt = 'The text to send to Slack.'
    parser.add_argument('text', action='store', type=str, help=help_txt)
    arguments = parser.parse_args()
    updater_utils.slack_msg(
        arguments.text,
        CONFIG.get('Slackbot', 'token'),
        CONFIG.get('Slackbot', 'default_channel')
    )


if __name__ == '__main__':
    main()
