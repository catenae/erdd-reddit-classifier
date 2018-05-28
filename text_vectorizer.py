#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
from catenae import Link, Electron, util


class TextVectorizer(Link):

    def setup(self):
        self.count_vectorizer = self.load_object('count_vectorizer')
        if not self.count_vectorizer:
            util.print_exception(self, "Could not load the count_vectorizer object.")

    def transform(self, electron):
        tic = timeit.default_timer()

        content = electron.value['submission_title'] + " " \
            + electron.value['content']

        # Identifiers are preserved so probabilities of individuals
        # texts an be stored
        electron.value['vector'] = self.count_vectorizer.transform([content])

        # The content and the title are not needed anymore
        electron.value.pop('content')
        electron.value.pop('submission_title')

        toc=timeit.default_timer()
        # print(toc - tic)

        return electron


if __name__ == "__main__":
    TextVectorizer().start()
