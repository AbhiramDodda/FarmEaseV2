const startRecordButton = document.getElementById("startRecord");
const stopRecordButton = document.getElementById("stopRecord");
const audioFileInput = document.getElementById("audioFile");

let mediaRecorder;
let audioChunks = [];

startRecordButton.addEventListener("click", () => {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const audioFile = new File([audioBlob], "recorded-audio.wav", {
          type: "audio/wav",
        });
        audioFileInput.files = [audioFile];
      };
      mediaRecorder.start();
      startRecordButton.disabled = true;
      stopRecordButton.disabled = false;
    })
    .catch((error) => {
      console.error("Error accessing microphone:", error);
    });
});

stopRecordButton.addEventListener("click", () => {
  mediaRecorder.stop();
  startRecordButton.disabled = false;
  stopRecordButton.disabled = true;
});
