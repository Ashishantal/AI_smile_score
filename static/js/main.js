let stream = null;
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const preview = document.getElementById("preview");
const saveBtn = document.getElementById("save");
const startBtn = document.getElementById("startCam");
const captureBtn = document.getElementById("capture");
const retakeBtn = document.getElementById("retake");
const closeCamBtn = document.getElementById("closeCam");

startBtn.onclick = async () => {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    video.style.display = "block";
    preview.style.display = "none";
    startBtn.style.display = "none";
    captureBtn.style.display = "inline-block";
    closeCamBtn.style.display = "inline-block";
};

closeCamBtn.onclick = () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        video.srcObject = null;
        video.style.display = "none";
        preview.style.display = "none";
        startBtn.style.display = "inline-block";
        captureBtn.style.display = "none";
        retakeBtn.style.display = "none";
        saveBtn.style.display = "none";
        closeCamBtn.style.display = "none";
    }
};

captureBtn.onclick = () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    preview.src = canvas.toDataURL("image/png");

    stream.getTracks().forEach(track => track.stop());
    stream = null;

    video.style.display = "none";
    preview.style.display = "block";

    captureBtn.style.display = "none";
    retakeBtn.style.display = "inline-block";
    saveBtn.style.display = "inline-block";
    closeCamBtn.style.display = "none";
};

retakeBtn.onclick = async () => {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    video.style.display = "block";
    preview.style.display = "none";
    captureBtn.style.display = "inline-block";
    retakeBtn.style.display = "none";
    saveBtn.style.display = "none";
    closeCamBtn.style.display = "inline-block";
};

if(saveBtn){
    saveBtn.onclick = () => {
        const dataURL = canvas.toDataURL("image/png");
        const csrfToken = document.getElementById("csrf-token").value;

        const form = document.createElement("form");
        form.method = "POST";
        form.style.display = "none";

        const csrfInput = document.createElement("input");
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = csrfToken;

        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "captured_image";
        input.value = dataURL;

        form.appendChild(csrfInput);
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    }
}
