import { useRef } from "react";
import api from "../services/api";

export default function UploadButton({ onUpload }) {
  const inputRef = useRef();

  const handleClick = () => {
    inputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
 
    
    try {
      const res = await api.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert(res.data.message);

      if (onUpload) {
        onUpload();
      }

    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    }
  };

  return (
    <>
      <button
        onClick={handleClick}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 rounded-lg py-3 font-semibold"
      >
        Upload PDF
      </button>

      <input
        type="file"
        accept=".pdf"
        hidden
        ref={inputRef}
        onChange={handleFileChange}
      />
    </>
  );
}