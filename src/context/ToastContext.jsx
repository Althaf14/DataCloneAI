import React, { createContext, useContext, useState, useCallback } from "react";
import { X, CheckCircle, AlertCircle, Info } from "lucide-react";
import { cn } from "../utils/cn";

const ToastContext = createContext(null);

export const ToastProvider = ({ children }) => {
    const [toasts, setToasts] = useState([]);

    const addToast = useCallback((message, type = "info") => {
        const id = Date.now() + Math.random();
        setToasts((prev) => [...prev, { id, message, type }]);

        // Auto remove after 5s
        setTimeout(() => {
            removeToast(id);
        }, 5000);
    }, []);

    const removeToast = useCallback((id) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ addToast, removeToast }}>
            {children}
            {/* Toast Container */}
            <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
                {toasts.map((toast) => (
                    <div
                        key={toast.id}
                        className={cn(
                            "pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg border transition-all animate-in slide-in-from-right-full fade-in duration-300 w-80",
                            toast.type === "success" && "bg-green-50 border-green-200 text-green-800",
                            toast.type === "error" && "bg-red-50 border-red-200 text-red-800",
                            toast.type === "info" && "bg-blue-50 border-blue-200 text-blue-800",
                            toast.type === "warning" && "bg-yellow-50 border-yellow-200 text-yellow-800"
                        )}
                    >
                        {toast.type === "success" && <CheckCircle size={20} />}
                        {toast.type === "error" && <AlertCircle size={20} />}
                        {toast.type === "info" && <Info size={20} />}
                        {toast.type === "warning" && <AlertCircle size={20} />}

                        <p className="text-sm font-medium flex-1">{toast.message}</p>

                        <button
                            onClick={() => removeToast(toast.id)}
                            className="opacity-50 hover:opacity-100 transition-opacity"
                        >
                            <X size={16} />
                        </button>
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    );
};

export const useToast = () => {
    const context = useContext(ToastContext);
    if (!context) {
        throw new Error("useToast must be used within a ToastProvider");
    }
    return context;
};
