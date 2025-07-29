document.getElementById("upload-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const fileInput = document.getElementById("file");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const status = document.getElementById("status");
  status.innerText = "Processing...";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    if (response.ok) {
      const blob = await response.blob();
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = "Processed_File.xlsx";
      link.click();
      status.innerText = "✅ Download ready!";
    } else {
      status.innerText = "❌ Processing failed.";
    }
  } catch (error) {
    status.innerText = "❌ Error occurred.";
  }
});
