chrome.history.onVisited.addListener((historyItem) => {
  console.log("Sending URL:", historyItem.url); // Add this line for debugging
  fetch("http://localhost:5000/log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: historyItem.url }),
  }).catch((error) => console.log("Error sending URL:", error)); // Catch any errors
});
