import React, { useState, useRef } from "react";
import { UploadCloud, File, X, CheckCircle } from "lucide-react";
import { Button } from "../components/ui/Button";
import { Progress } from "../components/ui/Progress";
import { useToast } from "../context/ToastContext";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function UploadPage() {
    const [file, setFile] = useState(null);
    const [docType, setDocType] = useState("id_proof"); // Default to ID Proof
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const fileInputRef = useRef(null);
    const { addToast } = useToast();
    const navigate = useNavigate();

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) validateAndSetFile(droppedFile);
    };

    const validateAndSetFile = (f) => {
        if (!f.type.startsWith("image/") && f.type !== "application/pdf") {
            addToast("Only images and PDFs are supported", "error");
            return;
        }
        setFile(f);
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setProgress(0);

        const formData = new FormData();
        formData.append("file", file);
        formData.append("doc_type", docType);

        try {
            // We can't easily get upload progress from axios with mock adapter in play previously,
            // but now we are real. Axios supports onUploadProgress.
            const response = await api.post("/api/documents/upload", formData, {
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(percentCompleted);
                }
            });

            addToast("File uploaded successfully", "success");

            // Navigate to report
            setTimeout(() => {
                navigate(`/report/${response.data.id}`);
            }, 500);

        } catch (error) {
            console.error(error);
            const msg = error.response?.data?.detail || "Upload failed";
            addToast(`Upload failed: ${msg}`, "error");
            setUploading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Upload Document</h1>
                <p className="text-muted-foreground">Upload identity documents or contracts for forgery analysis.</p>
            </div>

            {/* Document Type Selection */}
            <div className="bg-card border rounded-lg p-6 space-y-4">
                <label className="text-sm font-medium mb-2 block">Document Type</label>
                <div className="flex gap-4">
                    <button
                        onClick={() => setDocType("id_proof")}
                        className={`px-4 py-2 rounded-md border text-sm font-medium transition-colors ${docType === "id_proof"
                                ? "bg-primary text-primary-foreground border-primary"
                                : "bg-background hover:bg-accent hover:text-accent-foreground"
                            }`}
                    >
                        ID Proof (Generic)
                    </button>
                    <button
                        onClick={() => setDocType("certificate")}
                        className={`px-4 py-2 rounded-md border text-sm font-medium transition-colors ${docType === "certificate"
                                ? "bg-primary text-primary-foreground border-primary"
                                : "bg-background hover:bg-accent hover:text-accent-foreground"
                            }`}
                    >
                        Certificate / Contract
                    </button>
                </div>
                <p className="text-xs text-muted-foreground">
                    Selected analysis pipeline: <span className="font-semibold">{docType === "id_proof" ? "Identity Verification (Biometrics + OCR)" : "Document Integrity (Visual Forgery + Layout)"}</span>
                </p>
            </div>

            <div
                className={`
          border-2 border-dashed rounded-xl p-12 flex flex-col items-center justify-center text-center transition-colors
          ${isDragging ? "border-primary bg-primary/5" : "border-border hover:bg-accent/50"}
          ${uploading ? "opacity-50 pointer-events-none" : ""}
        `}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
                    <UploadCloud size={32} className="text-muted-foreground" />
                </div>

                <h3 className="text-lg font-semibold mb-2">
                    {file ? file.name : "Drag & drop your file here"}
                </h3>

                <p className="text-sm text-muted-foreground mb-6 max-w-sm">
                    Supported formats: JPEG, PNG, WEBP, PDF. Max file size: 10MB.
                </p>

                {!file ? (
                    <Button onClick={() => fileInputRef.current?.click()}>
                        Select File
                    </Button>
                ) : (
                    <div className="flex gap-2">
                        <Button variant="outline" onClick={() => setFile(null)} disabled={uploading}>
                            Change File
                        </Button>
                        <Button onClick={handleUpload} disabled={uploading} isLoading={uploading}>
                            {uploading ? "Uploading..." : "Start Analysis"}
                        </Button>
                    </div>
                )}

                <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    accept="image/*,application/pdf"
                    onChange={(e) => {
                        if (e.target.files?.[0]) validateAndSetFile(e.target.files[0])
                    }}
                />
            </div>

            {uploading && (
                <div className="space-y-2 animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <div className="flex justify-between text-sm font-medium">
                        <span>Uploading...</span>
                        <span>{progress}%</span>
                    </div>
                    <Progress value={progress} />
                </div>
            )}
        </div>
    );
}
