"""Main dialog that handles booking a flight."""
from typing import Final

from booking_details import BookingDetails
from botbuilder.core import BotTelemetryClient, MessageFactory, NullTelemetryClient
from botbuilder.dialogs import (
    ComponentDialog,
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt
from botbuilder.schema import InputHints
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import Intent, LuisHelper

from .booking_dialog import BookingDialog


class MainDialog(ComponentDialog):
    """Main dialog that handles booking a flight."""

    INITIAL_DIALOG_ID: Final[str] = "MainDialog"

    def __init__(
        self,
        luis_recognizer: FlightBookingRecognizer,
        booking_dialog: BookingDialog,
        telemetry_client: BotTelemetryClient = None,
    ):
        """Initialize the MainDialog with LuisRecognizer."""
        super().__init__(MainDialog.__name__)
        self.telemetry_client = telemetry_client or NullTelemetryClient()

        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = self.telemetry_client

        booking_dialog.telemetry_client = self.telemetry_client

        wf_dialog = WaterfallDialog(
            MainDialog.INITIAL_DIALOG_ID,
            [self.intro_step, self.act_step, self.final_step],
        )
        wf_dialog.telemetry_client = self.telemetry_client

        self._luis_recognizer = luis_recognizer
        self._booking_dialog_id = booking_dialog.id

        self.add_dialog(text_prompt)
        self.add_dialog(booking_dialog)
        self.add_dialog(wf_dialog)

        self.initial_dialog_id = MainDialog.INITIAL_DIALOG_ID

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Intro step for the main dialog.
        """
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the config.py file.",
                    input_hint=InputHints.ignoring_input,
                )
            )
            return await step_context.next(None)

        message_text = (
            str(step_context.options)
            if hasattr(step_context, "options") and step_context.options is not None
            else "Hello ! What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Act step for the main dialog.
        """
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._booking_dialog_id, BookingDetails()
            )

        # Call LUIS and gather any potential booking details. 
        # (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent in Intent.NOT_NONE_INTENTS:
            # Run the BookingDialog when no intent is recognized.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)
       
        """didnt_understand_text = (
            "Sorry, I didn't get that. Please try asking in a different way"
            )
        didnt_understand_message = MessageFactory.text(
                didnt_understand_text,
                didnt_understand_text,
                InputHints.ignoring_input,
            )
        await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)"""

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Final step for the main dialog.
        """
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            # Now we have all the booking details call the booking service.
            msg = "Great!!! So you can pack your bags"
            message = MessageFactory.text(msg, msg, InputHints.ignoring_input)
            await step_context.context.send_activity(message)


        prompt_message = "Do you want to book another trip ?"
        return await step_context.replace_dialog(self.id, prompt_message)
