const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const hiddenUpload = document.getElementById("hiddenUpload");
const form = document.getElementById("filterForm");

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => (video.srcObject = stream))
  .catch((err) => console.error("Error accessing webcam:", err));

function capture() {
  const ctx = canvas.getContext("2d");
  canvas.style.display = "block";
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob((blob) => {
    const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
    const dt = new DataTransfer();
    dt.items.add(file);
    hiddenUpload.files = dt.files;
  });
}
