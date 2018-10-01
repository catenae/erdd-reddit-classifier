#!/usr/bin/env python
# -*- coding: utf-8 -*-

from catenae import Link, Electron


class TfidfTransformer(Link):

    def setup(self):
        self.tfidf_transformer = self.load_object('tfidf_transformer')

    def transform(self, electron):
        # Remove extra information about the document if the input vector
        # is the aggregated vector of a user as is not needed anymore
        if 'aggregated' in electron.value:
            electron.value.pop('subreddit_id')
            electron.value.pop('timestamp')

        vector = electron.value['vector']
        electron.value['vector'] = self.tfidf_transformer.transform(vector)

        return electron


if __name__ == "__main__":
    TfidfTransformer().start(link_mode=Link.MULTIPLE_KAFKA_INPUTS, mki_mode='parity')
