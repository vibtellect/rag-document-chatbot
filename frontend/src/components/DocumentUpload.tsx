import { useState, useCallback } from "react";
import { Upload, File, Check, X, Loader2 } from "lucide-react";

interface UploadStatus {
  file: File;
  status: "uploading" | "success" | "error";
  message?: string;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function DocumentUpload() {
  const [uploads, setUploads] = useState<UploadStatus[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("tenant_id", "demo");

    try {
      const response = await fetch(`${API_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      return { success: true, message: `${data.chunks} Chunks erstellt` };
    } catch (error) {
      return { success: false, message: "Upload fehlgeschlagen" };
    }
  };

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files).filter((f) => {
      const lower = f.name.toLowerCase();
      return (
        lower.endsWith(".pdf") ||
        lower.endsWith(".md") ||
        lower.endsWith(".markdown")
      );
    });

    for (const file of files) {
      setUploads((prev) => [...prev, { file, status: "uploading" }]);

      const result = await uploadFile(file);

      setUploads((prev) =>
        prev.map((u) =>
          u.file === file
            ? {
                ...u,
                status: result.success ? "success" : "error",
                message: result.message,
              }
            : u,
        ),
      );
    }
  }, []);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []).filter((f) => {
      const lower = f.name.toLowerCase();
      return (
        lower.endsWith(".pdf") ||
        lower.endsWith(".md") ||
        lower.endsWith(".markdown")
      );
    });

    for (const file of files) {
      setUploads((prev) => [...prev, { file, status: "uploading" }]);

      const result = await uploadFile(file);

      setUploads((prev) =>
        prev.map((u) =>
          u.file === file
            ? {
                ...u,
                status: result.success ? "success" : "error",
                message: result.message,
              }
            : u,
        ),
      );
    }
  };

  const removeUpload = (file: File) => {
    setUploads((prev) => prev.filter((u) => u.file !== file));
  };

  return (
    <div className="upload-container">
      <div
        className={`dropzone ${isDragging ? "dragging" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <Upload size={48} className="icon" />
        <p className="title">PDF-Dokumente hierher ziehen</p>
        <p className="subtitle">oder klicken zum Auswählen</p>
        <input
          type="file"
          accept=".pdf,.md,.markdown"
          multiple
          onChange={handleFileSelect}
          className="file-input"
        />
      </div>

      <div className="uploads-list">
        {uploads.map((upload, i) => (
          <div key={i} className={`upload-item ${upload.status}`}>
            <File size={20} />
            <span className="filename">{upload.file.name}</span>

            {upload.status === "uploading" && (
              <Loader2 className="spinner" size={18} />
            )}
            {upload.status === "success" && (
              <Check size={18} className="success-icon" />
            )}
            {upload.status === "error" && (
              <X size={18} className="error-icon" />
            )}

            {upload.message && (
              <span className="message">{upload.message}</span>
            )}

            <button
              className="remove"
              onClick={() => removeUpload(upload.file)}
            >
              <X size={16} />
            </button>
          </div>
        ))}
      </div>

      <div className="info">
        <h3>Unterstützte Formate</h3>
        <ul>
          <li>PDF-Dokumente (.pdf)</li>
          <li>Markdown-Dateien (.md, .markdown)</li>
          <li>Maximale Größe: 50 MB</li>
          <li>Textbasierte PDFs liefern bessere Ergebnisse als reine Scans</li>
        </ul>
      </div>
    </div>
  );
}
