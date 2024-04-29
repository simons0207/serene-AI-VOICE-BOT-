import tempfile
from text2speech import text2speech
from speech2text import speech2text
from groq import Groq
from flask import Flask ,request, send_file,render_template,url_for

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("indexmain.html")

@app.route("/test")
def image():
    return render_template("omni.html")

@app.route("/divein")
def about():
    return render_template("index.html")

def video_stream():
    cap = cv2.VideoCapture('video.mp4')

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # You can process the frame here (e.g., resizing, adding overlays)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/video')
def video():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/process-audio",methods=["POST"])
def process_audio_data():
    audio_data=request.files["audio"].read()

    with tempfile.NamedTemporaryFile(delete=False,suffix='.wav') as temp_audio:
        temp_audio.write(audio_data)
        temp_audio.flush()

    text=speech2text(temp_audio.name)
    client = Groq(
    api_key="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"

    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"you are an emotional companion, help me with the following prompt '{text}' in less than 100 words"
            }
        ],
        model="mixtral-8x7b-32768",
    )
    generated_answer=(chat_completion.choices[0].message.content)
    generated_speech=text2speech(generated_answer)

    return send_file(generated_speech,mimetype='audio/mpeg')

  
if __name__ =='__main__':
    app.run(debug=True,port=8080)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")
