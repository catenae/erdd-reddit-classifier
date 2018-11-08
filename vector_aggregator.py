#!/usr/bin/env python
# -*- coding: utf-8 -*-

from catenae import Link, Electron


class VectorAggregator(Link):

    def transform(self, electron):
        """
        The previous vector is aggregated with the new one
        """

        vector = electron.value['vector']

        # Aggregated vector flag so it can be differenciated
        # with the vector of single document when it's processed
        # on the tfidf_transformer module
        electron.value['aggregated'] = True

        try:
            electron.value['vector'] = vector + \
                self.aerospike.get(electron.key,
                                   'test',
                                   'aggregated_count_vectors')[1]
        except:
            pass

        # Update the aggregated vector for the current user
        try:
            self.aerospike.put(electron.key,
                               electron.value,
                               'test',
                               'aggregated_count_vectors')
        except:
            pass

        return electron


if __name__ == "__main__":
    VectorAggregator().start()
