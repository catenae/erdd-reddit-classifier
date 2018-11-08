#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from catenae import Link, Electron, util


class AlertManager(Link):

    def _update_and_get_last_ids(self, electron):
        """
        Updates the last submission_id or comment_id depending on the type of
        the received text and returns the last submission_id and comment_id.
        """
        user_id = electron.key
        text_type = electron.value['type']

        # Submissions
        if text_type == 0:
            last_submission = electron.value['submission_id']

        # Comments
        elif text_type == 1:
            last_comment = electron.value['comment_id']

        # Overwrite the last submission_id received by the Alert Manager
        if text_type == 0:
            self.aerospike.put(user_id,
                               last_submission,
                               'test',
                               'alerts_last_submissions')

            # Last comment associated with the previous alert
            _, last_comment = self.aerospike.get(user_id,
                                                 'test',
                                                 'alerts_last_comments')

        # Overwrite the last comment_id received by the Alert Manager
        if text_type == 1:
            self.aerospike.put(user_id,
                               last_comment,
                               'test',
                               'alerts_last_comments')

            # Last submission associated with the previous alert
            _, last_submission = self.aerospike.get(user_id,
                                                    'test',
                                                    'alerts_last_submissions')

        return last_submission, last_comment

    def transform(self, electron):
        try:
            proba = electron.value['proba']
            last_submission, last_comment = self._update_and_get_last_ids(electron)

            if proba > .9:
                # Remove unnecessary attributes
                electron = Electron(electron.key, {'proba': proba})

                # Add new attributes
                timestamp = int(round(time.time() * 1000))
                electron.value['timestamp'] = timestamp
                electron.value['type'] = 'aggregation'
                electron.value['last_submission'] = last_submission
                electron.value['last_comment'] = last_comment

                if proba > .9:
                    electron.value['priority'] = 0
                elif proba > .8:
                    electron.value['priority'] = 1
                elif proba > .7:
                    electron.value['priority'] = 2
                elif proba > .6:
                    electron.value['priority'] = 3
                else:
                    electron.value['priority'] = 4

                # print(f"[ALERT P{electron.value['priority']}] {electron.key}")

                return electron
        except:
            print(electron.value)
            util.print_exception(self,
                                 "Unhandled exception. Exiting...",
                                 fatal=True)


if __name__ == "__main__":
    AlertManager().start()
