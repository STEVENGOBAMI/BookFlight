#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "b08408ec-2836-45f6-b7a1-e28b8aac264d")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "nar8Q~xAuSTRwwp4AdHZulTja-wEDCpooWp0pcja")
    LUIS_APP_ID = os.environ.get("LuisAppId", "cbcc3d00-8edb-4eed-9b11-fc7117272662")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "1d14d8fce23741f5a14f589af57ed107")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westus.api.cognitive.microsoft.com")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "2b57ad66-3a7f-4e7e-948b-76d45a9715a9"
    )
    # APP_ID = os.environ.get("MSAPP_ID", "")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    # APP_ID = None
    # APP_PASSWORD = None
    # LUIS_APP_ID = os.environ.get("LUIS_APPID", "")
    # LUIS_API_KEY = os.environ.get("AUTH_LUIS", "")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    # LUIS_API_HOST_NAME = os.environ.get("LUIS_APIHOST", "")
    # APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        # "INSIGHTS_KEY", ""
    # )
