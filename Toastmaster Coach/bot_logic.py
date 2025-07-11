# -*- coding: utf-8 -*-
import os, time, sys, random, json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes, Attachment
import uvicorn

#bot shell
app = FastAPI()

#Bot Credentials From Azure
# http://localhost:3978/api/messages
load_dotenv()
APP_ID = os.getenv("MICROSOFT_APP_ID")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")

settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    adapter.trust_service_url(activity.service_url)

    async def turn_handler(turn_context: TurnContext):

        #confirm incoming activity
        print("Conversation ID:", activity.conversation.id)
        print("Service URL:", activity.service_url)
        print("Recipient ID:", activity.recipient.id)

        if activity.type == ActivityTypes.message:
            reply = Activity(
                type=ActivityTypes.message,
                text="Hello Jasleen! Your bot is alive.",
                conversation=activity.conversation,
                recipient=activity.from_property,
                from_property=activity.recipient,
                reply_to_id=activity.id
            )
            await turn_context.send_activity("Hello Jasleen! Your bot is alive.")
        elif activity.type == ActivityTypes.conversation_update:
            await turn_context.send_activity("Welcome! Ready to coach you.")

    await adapter.process_activity(activity, auth_header, turn_handler)
    return {"status": "ok"}

#entry point for Teams messages
"""@app.post("/api/messages")
async def messages(req:Request):
    body = await req.json()
    activity = Activity().deserialize(body)

    async def turn_handler(turn_context: TurnContext):
        #only handles regular message or submit
        if activity.type == ActivityTypes.message:
            print("Activity type:", activity.type)
            print("Activity text:", activity.text)
            print("Activity value:", activity.value)
            print("Full activity:", activity.serialize())

            #grab action if present
            action = activity.value.get("action") if activity.value else None

            #route logic
            if action == "retry":
                await turn_context.send_activity(Activity(type="message", text="Retrying session..."))
            elif action == "progress":
                await turn_context.send_activity(Activity(type="message", text="Here's your progress summary..."))
            elif action == "continue":
                await turn_context.send_activity(Activity(type="message", text="Great job. Continuing to next session..."))
            else:
                #send default Adaptive Card
                card_json =build_sample_card()
                card_attachment = Attachment(
                    content_type="application/vnd.microsoft.card.adaptive",
                    content=card_json
                    )
                await turn_context.send_activity(Activity(
                    type="message",
                    attachments=[card_attachment]
                ))
        elif activity.type == ActivityTypes.conversation_update:
            await turn_context.send_activity("hello I am ready to coach you.")
    await adapter.process_activity(activity, activity.service_url, None, turn_handler)
    return {"status" : "ok"}

#Sample adaptive card generator
def build_sample_card():
    return {
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {"type": "TextBlock", "text": "Welcome to Jasleen's Feedback Bot", "weight": "Bolder", "size": "Medium"},
            {"type": "TextBlock", "text": "Click a button to begin or continue your coaching session", "wrap": True }
            ],
        "actions": [
            {"type": "Action.Submit", "title": "Retry", "data": {"action": "retry"}},
            {"type": "Action.Submit", "title": "View Progress", "data": {"action": "progress"}},
            {"type": "Action.Submit", "title": "Continue", "data": {"action": "continue"}}
            ]
        
        }
"""
 #run server locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3978)