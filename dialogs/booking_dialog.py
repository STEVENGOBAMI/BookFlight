"""Flight booking dialog."""

import requests
from botbuilder.core import BotTelemetryClient, MessageFactory, NullTelemetryClient
from botbuilder.core.bot_telemetry_client import Severity
from botbuilder.dialogs import DialogTurnResult, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import ConfirmPrompt, PromptOptions, TextPrompt
from botbuilder.schema import InputHints
from datatypes_date_time.timex import Timex

from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        """Initialize a new BookingDialog instance."""
        super().__init__(dialog_id or BookingDialog.__name__, telemetry_client)
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.or_city_step,
                self.dst_city_step,
                self.str_date_step,
                self.end_date_step,
                self.budget_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            DateResolverDialog(
                DateResolverDialog.__name__, self.telemetry_client
            )
        )
        # self.add_dialog(
            # DateResolverDialog(
            #     DateResolverDialog.END_DATE_DIALOG_ID, self.telemetry_client
            # )
        # )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def or_city_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for or_city."""
        booking_details = step_context.options

        if booking_details.or_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Where do you want to leave from ?")
                ),
            )

        return await step_context.next(booking_details.or_city)

    async def dst_city_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for dst_city."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.or_city = step_context.result.capitalize()

        if booking_details.dst_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Where do you want to go to ?")
                ),
            )

        return await step_context.next(booking_details.dst_city)

    async def str_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.dst_city = step_context.result.capitalize()

        if not booking_details.str_date or self.is_ambiguous(booking_details.str_date):
            return await step_context.begin_dialog(
                DateResolverDialog.START_DATE_DIALOG_ID,
                booking_details.str_date,
            )

        return await step_context.next(booking_details.str_date)

    async def end_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.str_date = step_context.result

        if not booking_details.end_date or self.is_ambiguous(booking_details.end_date):
            return await step_context.begin_dialog(
                DateResolverDialog.END_DATE_DIALOG_ID, booking_details.end_date
            )

        return await step_context.next(booking_details.end_date)

    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for travel budget."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.end_date = step_context.result

        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(
                        "How much do you want to spend on this trip ?"
                    )
                ),
            )

        return await step_context.next(booking_details.budget)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.budget = step_context.result
        msg = f"""
        Please confirm your booking details :
        from : **{booking_details.or_city} to : { booking_details.dst_city }**
        departure date : **{ booking_details.str_date } return date : { booking_details.end_date }**
        for a budget of : **{ booking_details.budget }**"""

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(
                    msg, msg, input_hint=InputHints.ignoring_input
                )
            ),
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""

        booking_details = step_context.options

        if step_context.result:
            self.telemetry_client.track_trace(
                "booking_accepted",
                properties=booking_details.__dict__,
            )

            return await step_context.end_dialog(booking_details)

        self.telemetry_client.track_trace(
            "booking_refused",
            severity=Severity.warning,
            properties=booking_details.__dict__,
        )

        return await step_context.end_dialog()

    @staticmethod
    def is_ambiguous(timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
