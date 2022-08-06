import json

import aiounittest
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.dialogs.prompts import TextPrompt

from booking_details import BookingDetails
from config import DefaultConfig
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import Intent, LuisHelper


class TestLuisHelper(aiounittest.AsyncTestCase):
    """Tests for the LUIS helper class"""

    async def test_execute_luis_query(self):
        """Tests the execute_luis_query method"""
        CONFIG = DefaultConfig()
        RECOGNIZER = FlightBookingRecognizer(CONFIG)

        async def exec_test(turn_context: TurnContext):
            """Executes the test"""
            # Call LUIS and gather any potential booking details. 
            # (Note the TurnContext has the response to the prompt.)
            intent, luis_result = await LuisHelper.execute_luis_query(
                RECOGNIZER, turn_context
            )
            await turn_context.send_activity(
                json.dumps(
                    {
                        "intent": intent,
                        "booking_details": luis_result.__dict__,
                    }
                )
            )

        adapter = TestAdapter(exec_test)

        await adapter.test(
            "Hello",
            json.dumps(
                {
                    "intent": Intent.INFO_INTENT,
                    "booking_details": BookingDetails().__dict__,
                }
            ),
        )

        await adapter.test(
            "I want to book a trip from London to Berlin for less than $1000.\
                 I will leave on the 2nd of August 2022 and come back to the 25 of August 2022.",
            json.dumps(
                {
                    "intent": Intent.INFO_INTENT,
                    "booking_details": BookingDetails(
                        or_city="London",
                        dst_city="Berlin",
                        str_date="2022-08-02",
                        end_date="2022-08-25",
                        budget="$1000",
                    ).__dict__,
                }
            ),
        )

        await adapter.test(
            "I want to book on the 1st October 2023 and come back to 15th October 2023.",
            json.dumps(
                {
                    "intent": Intent.INFO_INTENT,
                    "booking_details": BookingDetails(
                        str_date="2023-10-01",
                        end_date="2023-10-15",
                    ).__dict__,
                }
            ),
        )

        await adapter.test(
            "This book should cost less than $100.",
            json.dumps(
                {
                    "intent": Intent.INFO_INTENT,
                    "booking_details": BookingDetails(
                        budget="$100",
                    ).__dict__,
                }
            ),
        )
