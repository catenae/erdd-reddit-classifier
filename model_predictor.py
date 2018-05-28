#!/usr/bin/env python
# -*- coding: utf-8 -*-

import timeit
from catenae import Link, Electron


class ModelPredictor(Link):

    def setup(self):
        self.lr_model = self.load_object('lr_model')

    def transform(self, electron):
        tic = timeit.default_timer()

        vector = electron.value['vector']
        proba = self.lr_model.predict_proba(vector).item(1)
        electron.value['proba'] = proba

        # The vector is not needed anymore
        electron.value.pop('vector')

        # Topic order must be: user_proba (default), text_proba
        # The text_proba topic is assigned if the 'aggregated'
        # attribute is not present.
        if not 'aggregated' in electron.value:
            electron.topic = self.output_topics[1]

            # Processed texts +1
            stat_electron = Electron(electron.key,
                                     None,
                                     topic=self.output_topics[3])
        else:
            electron.value.pop('aggregated')
            # Processed users +1
            stat_electron = Electron(electron.key,
                                     None,
                                     topic=self.output_topics[2])

        toc=timeit.default_timer()
        # print(toc - tic)
        
        return [electron, stat_electron]


if __name__ == "__main__":
    ModelPredictor().start()
