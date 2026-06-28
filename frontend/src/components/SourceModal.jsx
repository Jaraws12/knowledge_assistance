import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

export default function SourceModal({ source, onClose }) {
  const [numPages, setNumPages] = useState(null);

  if (!source) return null;

  const pdfUrl = `http://localhost:8000/uploads/${encodeURIComponent(
    source.filename
  )}`;

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl w-[900px] h-[90vh] shadow-2xl flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex justify-between items-center px-6 py-4 border-b">
          <div>
            <h2 className="text-xl font-bold">
              📄 {source.filename}
            </h2>

            <p className="text-gray-500">
              Page {source.page}
            </p>
          </div>

          <button
            onClick={onClose}
            className="text-3xl font-bold hover:text-red-500"
          >
            ×
          </button>
        </div>

        {/* PDF Viewer */}
        <div className="flex-1 overflow-auto flex justify-center bg-gray-100 p-5">
          <Document
            file={pdfUrl}
            loading={<p>Loading PDF...</p>}
            error={<p className="text-red-500">Failed to load PDF.</p>}
            onLoadSuccess={({ numPages }) => {
              console.log("PDF loaded successfully");
              setNumPages(numPages);
            }}
            onLoadError={(err) => {
              console.error("PDF Load Error:", err);
            }}
            onSourceError={(err) => {
              console.error("PDF Source Error:", err);
            }}
          >
            <Page
              pageNumber={source.page}
              width={700}
              renderAnnotationLayer={true}
              renderTextLayer={true}
            />
          </Document>
        </div>

        {/* Footer */}
        <div className="border-t px-6 py-3 text-sm text-gray-500">
          {numPages
            ? `Showing page ${source.page} of ${numPages}`
            : "Loading..."}
        </div>
      </div>
    </div>
  );
}