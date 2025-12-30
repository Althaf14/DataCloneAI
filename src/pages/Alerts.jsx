import React, { useEffect, useState } from "react";
import api from "../services/api";
import { ShieldAlert, AlertTriangle, Info, Clock, Check } from "lucide-react";

import { useToast } from "../context/ToastContext";

export default function Alerts() {
    const { addToast } = useToast();
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/api/alerts")
            .then(res => {
                setAlerts(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch alerts", err);
                setLoading(false);
            });
    }, []);

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold tracking-tight">System Alerts</h1>

            <div className="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
                {loading ? (
                    <div className="p-8 text-center text-muted-foreground">Loading alerts...</div>
                ) : (
                    <div className="divide-y divide-border">
                        {alerts.map((alert) => (
                            <div key={alert.id} className="p-4 flex items-start gap-4 hover:bg-accent/50 transition-colors">
                                <div className={`mt-1 p-2 rounded-full ${alert.severity === 'high' ? 'bg-red-100 text-red-600' :
                                    alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                                        'bg-blue-100 text-blue-600'
                                    }`}>
                                    {alert.severity === 'high' ? <ShieldAlert size={20} /> :
                                        alert.severity === 'medium' ? <AlertTriangle size={20} /> :
                                            <Info size={20} />}
                                </div>
                                <div className="flex-1">
                                    <div className="flex justify-between items-start">
                                        <h4 className="font-semibold text-foreground">{alert.message}</h4>
                                        <span className="text-xs text-muted-foreground flex items-center gap-1">
                                            <Clock size={12} /> {alert.timestamp}
                                        </span>
                                    </div>
                                    <p className="text-sm text-muted-foreground capitalize mt-1">
                                        Type: {alert.type} • Severity: {alert.severity}
                                    </p>
                                </div>
                                <div className="self-center">
                                    <button
                                        onClick={() => addToast("Alert details feature coming soon", "info")}
                                        className="text-xs font-medium text-primary hover:underline"
                                    >
                                        Details
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
