export const sendImage = async (imageBlob) => {  
    try {
      const response = await fetch("", {
        method: "POST",
        body: imageBlob,
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
      console.error("Error sending image:", error);
    }
  };
  