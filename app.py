import os
import logging
import logging.config

import yaml
import responder

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger("Bot")


line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

api = responder.API()

@api.route("/callback")
class Callback:
    async def on_post(self, req, resp):
        signature = req.headers["X-Line-Signature"]
        body = await req.text
        logger.info("Req body: %s ", body)
        try:
            handler.handle(body, signature)
            resp.text = "OK"
        except InvalidSignatureError:
            logger.debug("failed")
            resp.status_code = 400

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    api.run(port=5000)
