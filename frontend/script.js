let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Get UI elements
const recordBtn = document.getElementById("recordBtn");
const recordStatus = document.getElementById("recordStatus");

// Start / Stop button
recordBtn.addEventListener("click", async () => {
    if (!isRecording) {
        await startRecording();
    } else {
        stopRecording();
    }
});


// ===============================
// START RECORDING
// ===============================
async function startRecording() {
    try {
        // Ask for microphone access
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        console.log("Microphone stream obtained.");
        console.log("Audio tracks:", stream.getAudioTracks().length);

        audioChunks = [];

        // Check which audio formats the browser supports
        const mimeTypes = [
            "audio/webm;codecs=opus",
            "audio/webm",
            "audio/ogg;codecs=opus"
        ];

        const supportedType = mimeTypes.find(type =>
            MediaRecorder.isTypeSupported(type)
        );

        console.log("Supported MIME type:", supportedType);

        if (!supportedType) {
            throw new Error("No supported audio recording format found.");
        }

        // Create recorder using supported format
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: supportedType
        });

        console.log(
            "Actual recorder MIME type:",
            mediaRecorder.mimeType
        );

        // Receive recorded audio chunks
        mediaRecorder.ondataavailable = event => {

            console.log(
                "Audio chunk received:",
                event.data.size,
                "bytes"
            );

            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };


        // When recording stops
        mediaRecorder.onstop = async () => {

            console.log(
                "Number of audio chunks:",
                audioChunks.length
            );

            // Create final audio blob
            const audioBlob = new Blob(audioChunks, {
                type: mediaRecorder.mimeType
            });

            console.log(
                "Final audio size:",
                audioBlob.size,
                "bytes"
            );

            console.log(
                "Final audio type:",
                audioBlob.type
            );

            if (audioBlob.size === 0) {
                console.error("Final audio blob is empty.");

                recordStatus.textContent =
                    "No audio was recorded.";

                stream.getTracks().forEach(track => track.stop());

                return;
            }

            // Send audio to backend
            await sendAudio(audioBlob);

            // Stop microphone
            stream.getTracks().forEach(track => track.stop());

            console.log("Microphone stopped.");
        };


        // Start recording
        mediaRecorder.start();

        isRecording = true;

        recordBtn.textContent = "⏹️ Stop Recording";

        recordStatus.textContent =
            "Listening... Speak now";

        console.log("Recording started.");

    } catch (error) {

        console.error(
            "Recording error:",
            error
        );

        recordStatus.textContent =
            "Microphone permission denied or recording failed.";

        isRecording = false;
    }
}


// ===============================
// STOP RECORDING
// ===============================
function stopRecording() {

    if (!mediaRecorder) {
        console.warn("MediaRecorder does not exist.");
        return;
    }

    if (mediaRecorder.state === "recording") {

        console.log("Stopping recording...");

        mediaRecorder.stop();

        isRecording = false;

        recordBtn.textContent =
            "🎤 Start Recording";

        recordStatus.textContent =
            "Processing your grievance...";
    }
}


// ===============================
// SEND AUDIO TO BACKEND
// ===============================
async function sendAudio(audioBlob) {

    if (!audioBlob || audioBlob.size === 0) {

        console.error("Audio blob is empty.");

        recordStatus.textContent =
            "No audio recorded.";

        return;
    }


    console.log("==============================");
    console.log("Sending audio to backend");
    console.log("Audio size:", audioBlob.size);
    console.log("Audio type:", audioBlob.type);
    console.log("==============================");


    const formData = new FormData();


    // Determine file extension
    let extension = "webm";

    if (audioBlob.type.includes("ogg")) {
        extension = "ogg";
    }


    // Add audio file
    formData.append(
        "audio",
        audioBlob,
        `voice.${extension}`
    );


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/grievances/Voice",
            {
                method: "POST",
                body: formData
            }
        );


        console.log(
            "Backend HTTP status:",
            response.status
        );


        // ===============================
        // BACKEND ERROR
        // ===============================
        if (!response.ok) {

            const errorText =
                await response.text();

            console.error(
                "STATUS:",
                response.status
            );

            console.error(
                "BACKEND RESPONSE:",
                errorText
            );

            recordStatus.textContent =
                "Could not understand audio.";

            return;
        }


        // ===============================
        // SUCCESS RESPONSE
        // ===============================
        const data = await response.json();

        console.log(
            "Server response:",
            data
        );


        // ===============================
        // DISPLAY TRANSCRIPTION
        // ===============================
        const transcription =
            document.getElementById("transcription");

        if (transcription) {
            transcription.textContent =
                data.text || "-";
        }


        // ===============================
        // DISPLAY LANGUAGE
        // ===============================
        const language =
            document.getElementById("language");

        if (language) {
            language.textContent =
                data.language || "-";
        }


        // ===============================
        // DISPLAY CATEGORY
        // ===============================
        const category =
            document.getElementById("category");

        if (category) {
            category.textContent =
                data.category || "-";
        }


        // ===============================
        // DISPLAY DEPARTMENT
        // ===============================
        const department =
            document.getElementById("department");

        if (department) {
            department.textContent =
                data.department || "-";
        }


        // ===============================
        // DISPLAY PRIORITY
        // ===============================
        const priority =
            document.getElementById("priority");

        if (priority) {
            priority.textContent =
                data.priority || "-";
        }


        // ===============================
        // DISPLAY GRIEVANCE ID
        // ===============================
        const grievanceId =
            document.getElementById("grievanceId");

        if (grievanceId) {
            grievanceId.textContent =
                data.grievance_id || "-";
        }


        // ===============================
        // DISPLAY RESPONSE TEXT
        // ===============================
        const responseText =
            document.getElementById("responseText");

        if (responseText) {
            responseText.textContent =
                data.response_text || "-";
        }


        // ===============================
        // RESPONSE AUDIO
        // ===============================
        if (data.audio_url) {

            const audio =
                document.getElementById(
                    "responseAudio"
                );

            if (audio) {

                audio.src =
                    "http://127.0.0.1:8000" +
                    data.audio_url;

                audio.style.display =
                    "block";

                audio.load();

                // Try autoplay
                audio.play().catch(error => {

                    console.log(
                        "Autoplay blocked:",
                        error
                    );

                });
            }
        }


        // ===============================
        // SUCCESS MESSAGE
        // ===============================
        recordStatus.textContent =
            "Grievance successfully registered";


    } catch (error) {

        console.error(
            "Voice grievance error:",
            error
        );

        recordStatus.textContent =
            "Could not process the grievance.";
    }
}