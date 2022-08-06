CoreBot with Application Insights (https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/21.corebot-app-insights)
Bot Framework v4 core bot sample.

This bot has been created using Bot Framework, it shows how to:

Use LUIS to implement core AI capabilities
Implement a multi-turn conversation using Dialogs
Handle user interruptions for such things as Help or Cancel
Prompt for and validate requests for information from the user
Use Application Insights to monitor your bot
Prerequisites
This sample requires prerequisites in order to run.

Overview
This bot uses LUIS, an AI based cognitive service, to implement language understanding and Application Insights, an extensible Application Performance Management (APM) service for web developers on multiple platforms.

Create a LUIS Application to enable language understanding
LUIS language model setup, training, and application configuration steps can be found here.

If you wish to create a LUIS application via the CLI, these steps can be found in the README-LUIS.md.

Add Application Insights service to enable the bot monitoring
Application Insights resource creation steps can be found here.

You must include the instrumentation key in the config.py file, as well is in the designated field in your Azure Bot resource.

Add Activity and Personal Information logging for Application Insights
To log activity and personal information, extra code is needed in app.py after the creation of the telemetry client. This code is already present in the sample, but must be unconmmented in order to function. It is important to note that due to privacy concerns, in a real-world application you must obtain user consent prior to logging this information.

The required code is as follows:

TELEMETRY_LOGGER_MIDDLEWARE = TelemetryLoggerMiddleware(telemetry_client=TELEMETRY_CLIENT, log_personal_information=True)
ADAPTER.use(TELEMETRY_LOGGER_MIDDLEWARE)
To try this sample
Clone the repository
git clone https://github.com/STEVENGOBAMI/BookFlight.git
In a terminal, navigate to fligth-booking-bot folder
Activate your desired virtual environment
In the terminal, type pip install -r requirements.txt
Run your bot with python app.py
Testing the bot using Bot Framework Emulator
Bot Framework Emulator is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

Install the latest Bot Framework Emulator from here
Connect to the bot using Bot Framework Emulator
Launch Bot Framework Emulator
File -> Open Bot
Enter a Bot URL of http://localhost:3978/api/messages
Deploy the bot to Azure
To learn more about deploying a bot to Azure, see Deploy your bot to Azure for a complete list of deployment instructions.

Further reading
Bot Framework Documentation
Bot Basics
Dialogs
Gathering Input Using Prompts
Activity processing
Azure Bot Service Introduction
Azure Bot Service Documentation
Azure CLI
Azure Portal
Language Understanding using LUIS
Channels and Bot Connector Service
Application insights Overview
Getting Started with Application Insights
Filtering and preprocessing telemetry in the Application Insights SDK