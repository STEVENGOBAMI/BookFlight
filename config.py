#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    # APP_ID = os.environ.get("MicrosoftAppId", "")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LUIS_APPID", "")
    LUIS_API_KEY = os.environ.get("AUTH_LUIS", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("AUTH_ENDPOINT", "")
    #APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        #"AppInsightsInstrumentationKey", ""
    #)
