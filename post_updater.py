#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
from catenae import Link, Electron, util
from pymongo import MongoClient
from conf import conf_loader as conf


class PostUpdater(Link):

    def setup(self):
        self.mongo_client = MongoClient(conf.mongo['address'], conf.mongo['port'])
        self.db = self.mongo_client.reddit_early_risk
        self.submissions = self.db.submissions
        self.comments = self.db.comments

        # Ensure submissions indices
        self.submissions.create_index('submission_id', unique=True, background=True)
        self.submissions.create_index('author', unique=False, background=True)
        self.submissions.create_index('subreddit_id', unique=False, background=True)
        self.submissions.create_index('timestamp', unique=False, background=True)

        # Ensure comments indices
        self.comments.create_index('comment_id', unique=True, background=True)
        self.comments.create_index('author', unique=False, background=True)
        self.comments.create_index('subreddit_id', unique=False, background=True)
        self.comments.create_index('timestamp', unique=False, background=True)


    def transform(self, electron):
        tic = timeit.default_timer()

        try:
            proba = {'proba': electron.value['proba']}

            if electron.value['type'] == 0:
                self.submissions.update_one(
                    {"submission_id": electron.value['submission_id']},
                    {"$set": proba},
                    upsert=True)
            elif electron.value['type'] == 1:
                self.comments.update_one(
                    {"comment_id": electron.value['comment_id']},
                    {"$set": proba},
                    upsert=True)
        except:
            self.mongo_client.close()
            util.print_exception(self,
                f"Unhandled exception. Value: {electron.value}Exiting...",
                fatal=True)

        toc=timeit.default_timer()
        # print(toc - tic)


if __name__ == "__main__":
    PostUpdater().start(link_mode=Link.CUSTOM_OUTPUT)
