from flask import Flask, request, send_file, render_template
import tempfile
from text2speech import text2speech
from speech2text import speech2text
from groq import Groq

client = Groq(
    api_key="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"
)
output=speech2text("output.wav")
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Please translate {output} to malayalam"
        }
    ],
    model="mixtral-8x7b-32768",
)
(chat_completion.choices[0].message.content)
