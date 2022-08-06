import json

import aiounittest
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.dialogs.prompts import TextPrompt

from booking_details import BookingDetails
from config import DefaultConfig
from dialogs import BookingDialog, MainDialog
from flight_booking_recognizer import FlightBookingRecognizer
from botbuilder.schema import InputHints



class MainDialogTest(aiounittest.AsyncTestCase):
    """Tests for the main dialog"""

    async def test_booking_dialog(self):
        """Tests the booking dialog"""

        async def exec_test(turn_context: TurnContext):
            """Executes the test"""
            dialog_context = await dialogs.create_context(turn_context)
            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                await main_dialog.intro_step(dialog_context)

            elif results.status == DialogTurnStatus.Complete:
                # reply = results.result
                await main_dialog.act_step(dialog_context)

            await conv_state.save_changes(turn_context)

        conv_state = ConversationState(MemoryStorage())
        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        booking_dialog = BookingDialog()
        main_dialog = MainDialog(
            FlightBookingRecognizer(DefaultConfig()), booking_dialog
        )
        dialogs.add(booking_dialog)

        text_prompt = await main_dialog.find_dialog(TextPrompt.__name__)
        dialogs.add(text_prompt)

        wf_dialog = await main_dialog.find_dialog(MainDialog.INITIAL_DIALOG_ID)
        dialogs.add(wf_dialog)

        adapter = TestAdapter(exec_test)

        await adapter.test("Hi!", "Hello ! What can I help you with today?")

        await adapter.test("Book a flight", "🛫 From where do you want to leave ? (eg : London)")
        await adapter.test("Paris", "🛬 Where do you want to go ? (eg : Paris)")
        await adapter.test("London", "What date do you want to leave 🥳 ?")
        await adapter.test("2023-01-01", "Please indicate your desired return date 😮‍💨")
        await adapter.test(
            "2023-01-17",
            "💸 What is your budget for this trip ? (eg : $500)",
        )
        await adapter.test(
            "$100",
            """Please confirm your trip details :
- 🛫 from : **Paris**
- 🛬 to : **London**
- 🥳 departure date : **2023-01-01**
- 😮‍💨 return date : **2023-01-17**
- 💸 for a budget of : **$100** (1) Yes or (2) No""",
            )