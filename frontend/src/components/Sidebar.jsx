import { useEffect, useState } from "react";
import api from "../services/api";
import UploadButton from "./UploadButton";

export default function Sidebar() {
  const [documents, setDocuments] = useState([]);

  const loadDocuments = async () => {
    try {
      const res = await api.get("/documents");
      setDocuments(res.data.documents);
    } catch (err) {
      console.error(err);
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
                className="bg-slate-800 rounded-lg p-3 mb-3"
              >
                <div className="font-semibold">
                  {doc.filename}
                </div>

                <div className="text-sm text-slate-400">
                  {doc.chunks} chunks
                </div>
              </div>
            ))
          )
        }

      </div>

    </div>
  );
}