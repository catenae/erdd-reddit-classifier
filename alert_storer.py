#!/usr/bin/env python
# -*- coding: utf-8 -*-

from catenae import Link, Electron, util
from pymongo import MongoClient
from conf import conf_loader as conf


class AlertStorer(Link):

    def setup(self):
        self.mongo_client = MongoClient(conf.mongo['address'], conf.mongo['port'])
        self.db = self.mongo_client.reddit_early_risk
        self.alerts = self.db.alerts
        self.users = self.db.users

        # Ensure alerts indices
        self.alerts.create_index('user', unique=False, background=True)
        self.alerts.create_index('priority', unique=False, background=True)
        self.alerts.create_index('timestamp', unique=False, background=True)
        self.alerts.create_index('proba', unique=False, background=True)

        # Ensure users index
        self.users.create_index('nickname', unique=True, background=True)

    def transform(self, electron):
        try:
            alert = {'user': electron.key,
                     'priority': electron.value['priority'],
                     'proba': electron.value['proba'],
                     'type': electron.value['type'],
                     'last_submission': electron.value['last_submission'],
                     'last_comment': electron.value['last_comment'],
                     'timestamp': electron.value['timestamp']}
            self.alerts.insert_one(alert)

            status = alert
            status.pop('user')
            status.pop('type')
            # status['risk'] = True
            self.users.update_one(
                { 'nickname': electron.key },
                { '$set': { 'status': status } },
                upsert=True)

        except Exception:
            util.print_exception(self,
                f"Unhandled exception. Value: {electron.value}. Exiting...",
                fatal=True)


if __name__ == '__main__':
    AlertStorer().start(link_mode=Link.CUSTOM_OUTPUT)
