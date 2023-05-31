#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "c3cb6451-dc5b-4908-83cb-63bbe0772bdb")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "lkp8Q~Dh3OKQdspqlBzuDTzgSZsn5c4.BtkCzc7z")
