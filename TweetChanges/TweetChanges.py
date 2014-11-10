#!/usr/bin/env python
#
# Copyright 2010 Per Olofsson, 2013 Greg Neagle, 2014 Nate Walck
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import twitter

from autopkglib import Processor, ProcessorError


__all__ = ["TweetChanges"]


class TweetChanges(Processor):
    description = "Tweets the latest version of the app."
    input_variables = {
        "app_name": {
            "required": True,
            "description":
                "Name of the app that has an update.",
        },
        "version": {
            "required": True,
            "description": ("Version of the app that has an update."),
        },
    }
    output_variables = {
    }

    __doc__ = description


    def load_app_keys(self):
        """Load app keys from a file on disk"""
        twitter_app_keys_path = os.path.expanduser('~/.twitter_app_keys')
        with open (twitter_app_keys_path) as f:
            credentials = [x.strip().split(':') for x in f.readlines()]

        return credentials[0]

    def tweet(self, app_name, version):
        MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_oauth')
        CONSUMER_KEY, CONSUMER_SECRET = self.load_app_keys()

        if not os.path.exists(MY_TWITTER_CREDS):
            twitter.oauth_dance("autopkgsays", CONSUMER_KEY, CONSUMER_SECRET,
                        MY_TWITTER_CREDS)
        oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)
        twitter_instance = twitter.Twitter(auth=twitter.OAuth(
            oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
        # Now work with Twitter
        twitter_instance.statuses.update(status="%s version %s has been released" % (app_name, version))

    def main(self):
        # Determine product_name, release, locale, and base_url.
        app_name = self.env["app_name"]
        version = self.env["version"]
        try:
            self.tweet(app_name, version)
            self.output("Tweeted %s has been updated to %s" % (self.env["app_name"], self.env["version"]))
        except:
            self.output("Duplicate Tweet or Failed for another reason")


if __name__ == "__main__":
    processor = TweetChanges()
    processor.execute_shell()

