import { useEffect, useState } from "react";
import api from "../services/api";
import UploadButton from "./UploadButton";

export default function Sidebar({
  selectedDocuments,
  setSelectedDocuments,
}) {
  const [documents, setDocuments] = useState([]);

  const loadDocuments = async () => {
    try {
      const res = await api.get("/documents");
      setDocuments(res.data.documents);
      setSelectedDocuments(
  res.data.documents.map((doc) => doc.filename)
);
    } catch (err) {
      console.error(err);
    }
  };

const handleDelete = async (filename) => {

  const confirmDelete = window.confirm(
    `Delete "${filename}"?`
  );

  if (!confirmDelete) return;

  try {

    await api.delete(`/documents/${encodeURIComponent(filename)}`);

    setDocuments((prev) =>
      prev.filter((doc) => doc.filename !== filename)
    );

  } catch (err) {
    console.error(err);
    alert("Failed to delete document.");
  }
};  

  useEffect(() => {
    loadDocuments();
  }, []);

  return (
    <div className="w-80 bg-slate-900 border-r border-slate-700 p-5">

      <h1 className="text-2xl font-bold">
        Knowledge Assistant
      </h1>

      <p className="text-slate-400 mt-2">
        Upload PDFs and chat with them.
      </p>

      <UploadButton onUpload={loadDocuments} />

      <div className="mt-8">

        <h2 className="text-lg font-semibold mb-3">
          Documents
        </h2>

        {
          documents.length === 0 ? (
            <p className="text-slate-400">
              No documents uploaded.
            </p>
          ) : (
            documents.map((doc, index) => (
              <div
  key={index}
  className="bg-slate-800 rounded-lg p-3 mb-3 flex justify-between items-center"
>

  <label className="flex items-center gap-3 flex-1 cursor-pointer">

    <input
      type="checkbox"
      checked={selectedDocuments.includes(doc.filename)}
      onChange={(e) => {

        if (e.target.checked) {

          setSelectedDocuments((prev) => [
            ...prev,
            doc.filename,
          ]);

        } else {

          setSelectedDocuments((prev) =>
            prev.filter(
              (name) => name !== doc.filename
            )
          );

        }

      }}
    />

    <div>

      <div className="font-semibold">
        📄 {doc.filename}
      </div>

      <div className="text-sm text-slate-400">
        {doc.chunks} chunks
      </div>

    </div>

  </label>

  <button
    onClick={() => handleDelete(doc.filename)}
    className="text-red-400 hover:text-red-600 text-lg ml-3"
  >
    🗑
  </button>

</div>
            ))
          )
        }

      </div>

    </div>
  );
}