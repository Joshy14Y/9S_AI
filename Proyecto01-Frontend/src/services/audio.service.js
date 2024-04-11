export const sendAudio = async (audioBlob) => {  
    try {
      const response = await fetch("/transcribe", {
        method: "POST",
        body: audioBlob,
        headers: {
          "Content-Type": "audio/wav"
        }
      });
  
      if (!response.ok) {
        throw new Error("Error in the request");
      }
  
      const data = await response.json(); 
      console.log("Server response:", data);
  
    } catch (error) {
      console.error("Error sending audio:", error);
    }
  };
  