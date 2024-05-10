import os

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)


# Path to the audio file


def speech2text(audio_file):
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient("########")

        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        return (transcript)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    print(speech2text("output.wav"))
