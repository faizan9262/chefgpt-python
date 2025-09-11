import axios from "axios";

export const generateImage = async (prompt: string) => {
  console.log(prompt)
  try {
    const response = await axios.post("/suggest/generate-image", {
      text: prompt, // send prompt text to backend
    });

    if (response.status !== 200) {
      console.log("Something went wrong while generating image.");
      return null;
    }

    // Return the actual image URL from backend
    return response.data.image_url;
  } catch (error) {
    console.log("Error generating image:", error);
    return null;
  }
};
