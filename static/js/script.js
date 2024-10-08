document.addEventListener('DOMContentLoaded', async () => {
    const recordingIndicator = document.getElementById('recordingIndicator');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    let mediaRecorder;
    let recordChunks = [];

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) recordChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(recordChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('audio', audioBlob);

            try {
                const response = await fetch('/process-audio', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    console.log('Audio uploaded successfully');
                    const returnedBlob = await response.blob();
                    const returnedURL = URL.createObjectURL(returnedBlob);
                    new Audio(returnedURL).play();
                } else {
                    console.error('Server error:', response.statusText);
                }
            } catch (error) {
                console.error('Upload failed:', error);
            }
        };
    } catch (error) {
        console.error('Failed to get media:', error);
    }

    startButton.addEventListener('click', () => {
        startButton.style.display = 'none';
        stopButton.style.display = 'block';
        if (mediaRecorder.state === 'inactive' || mediaRecorder.state === 'paused') {
            mediaRecorder.start();
            // recordingIndicator.style.display = 'block';
            // recordChunks = []; // Clear the previous data
            console.log('Recording started');
        }
    });

    stopButton.addEventListener('click', () => {
        stopButton.style.display = 'none';
        startButton.style.display = 'block';
        if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            recordingIndicator.style.display = 'none';
        }
    });
}
);