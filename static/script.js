document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/upload", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  const downloadLink = document.getElementById("downloadLink");
  const downloadBtn = document.getElementById("downloadBtn");

  if (data.download_url) {
    downloadBtn.href = data.download_url;
    downloadLink.style.display = 'block';
  } else {
    alert("Error processing file.");
  }
});
