// The URL of FastAPI backend
const BASE_URL = "http://localhost:8000";

export async function reviewPR(prUrl, focusAreas) {
  // Send POST request to FastAPI backend
  const response = await fetch(`${BASE_URL}/api/review`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      pr_url: prUrl,
      focus_areas: focusAreas,
    }),
  });

  // If something went wrong, throw an error with the detail message
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Review request failed");
  }

  // Return the JSON response
  return response.json();
}