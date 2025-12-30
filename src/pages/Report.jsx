import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { ImageViewer } from "../components/features/ImageViewer";
import { Button } from "../components/ui/Button";
import { AlertCircle, CheckCircle2, SlidersHorizontal, Eye, EyeOff, BarChart2, Download } from "lucide-react";
import api from "../services/api";
import { useToast } from "../context/ToastContext";
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default function ReportPage() {
    const { id } = useParams();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [heatmapOpacity, setHeatmapOpacity] = useState(0.6);
    const [showHeatmap, setShowHeatmap] = useState(true);
    const { addToast } = useToast();
    const reportRef = useRef(null); // Ref for PDF capture

    useEffect(() => {
        const fetchReport = async () => {
            try {
                setLoading(true);
                const res = await api.get(`/api/documents/${id}/report`);
                setData(res.data);
            } catch (e) {
                addToast("Failed to load report", "error");
            } finally {
                setLoading(false);
            }
        };
        fetchReport();
    }, [id, addToast]);

    const handleDownloadPDF = async () => {
        if (!reportRef.current) return;

        try {
            addToast("Generating PDF...", "info");
            const canvas = await html2canvas(reportRef.current, { scale: 2 });
            const imgData = canvas.toDataURL("image/png");
            const pdf = new jsPDF("p", "mm", "a4");
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

            pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
            pdf.save(`dataclone_report_${id}.pdf`);
            addToast("PDF Downloaded", "success");
        } catch (e) {
            console.error(e);
            addToast("PDF Generation Failed", "error");
        }
    };

    if (loading) return <div className="p-8 text-center">Loading analysis...</div>;
    if (!data) return <div className="p-8 text-center text-destructive">Report not found</div>;

    // Prepare Chart Data (Impact Analysis)
    const moduleData = data.module_reports?.raw?.pipeline_results?.map(res => {
        // Prefer confidence_impact (-20), fallback to converted score
        let impact = res.confidence_impact !== undefined ? res.confidence_impact :
            (res.score !== undefined ? (res.score - 1) * 100 : 0);

        return {
            name: res.module?.replace('Detection', '')?.replace('Module', '')?.replace('& Pre-Processing', '')?.trim(),
            score: impact,
            signal_strength: res.signal_strength
        };
    }) || [];

    // Gauge Data
    const gaugeData = [
        { name: 'Confidence', value: Math.round(data.confidence_score * 100) },
        { name: 'Penalty', value: 100 - Math.round(data.confidence_score * 100) }
    ];
    const COLORS = ['#22c55e', '#ef4444']; // Green, Red
    if (data.confidence_score < 0.6) COLORS[0] = '#ef4444'; // Red
    else if (data.confidence_score < 0.85) COLORS[0] = '#eab308'; // Yellow


    return (
        <div className="space-y-6 pb-12" ref={reportRef}>
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div className="flex items-center gap-2 mb-1">
                        <h1 className="text-3xl font-bold tracking-tight">Analysis Report</h1>
                        <span className={`px-2 py-1 rounded text-xs font-bold uppercase tracking-wider ${data.status === 'verified' || data.confidence_score === 1.0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                            }`}>
                            {data.module_reports?.raw?.risk_summary?.risk_level || data.status}
                        </span>
                    </div>
                    <p className="text-muted-foreground flex items-center gap-2 text-sm">
                        ID: {data.id} • {data.doc_type?.replace('_', ' ').toUpperCase()} • {new Date(data.upload_date).toLocaleDateString()}
                    </p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" onClick={handleDownloadPDF} className="gap-2">
                        <Download size={16} /> Save PDF
                    </Button>
                    <Button onClick={() => addToast("Document marked as verified!", "success")}>
                        Mark as Verified
                    </Button>
                </div>
            </div>

            {/* Explainability Section - "Why flagged" */}
            {data.module_reports?.raw?.risk_summary && (
                <div className={`rounded-xl border p-4 flex items-start gap-4 ${data.module_reports.raw.risk_summary.risk_level === 'SAFE'
                        ? 'bg-green-50 border-green-200'
                        : data.module_reports.raw.risk_summary.risk_level === 'LOW'
                            ? 'bg-yellow-50 border-yellow-200'
                            : 'bg-red-50 border-red-200'
                    }`}>
                    <AlertCircle className={`mt-0.5 shrink-0 ${data.module_reports.raw.risk_summary.risk_level === 'SAFE' ? 'text-green-600' : 'text-red-600'
                        }`} size={20} />
                    <div>
                        <h3 className={`font-semibold text-sm mb-1 ${data.module_reports.raw.risk_summary.risk_level === 'SAFE' ? 'text-green-800' : 'text-red-800'
                            }`}>
                            Analyst Summary: {data.module_reports.raw.risk_summary.risk_level} RISK
                        </h3>
                        <p className={`text-sm ${data.module_reports.raw.risk_summary.risk_level === 'SAFE' ? 'text-green-700' : 'text-red-700'
                            }`}>
                            {data.module_reports.raw.risk_summary.summary}
                        </p>
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Left Col: Image Viewer */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-card border border-border rounded-xl p-1 shadow-sm overflow-hidden">
                        <div className="p-3 border-b border-border flex justify-between items-center bg-muted/20">
                            <h3 className="font-semibold text-sm">Visual Inspection</h3>
                            <div className="flex items-center gap-2">
                                <span className="text-xs text-muted-foreground mr-2">Heatmap Opacity</span>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.1"
                                    value={heatmapOpacity}
                                    onChange={(e) => setHeatmapOpacity(parseFloat(e.target.value))}
                                    className="w-20 h-1 bg-secondary rounded-lg appearance-none cursor-pointer"
                                />
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => setShowHeatmap(!showHeatmap)}
                                    className={showHeatmap ? "text-primary text-xs" : "text-muted-foreground text-xs"}
                                >
                                    {showHeatmap ? <Eye size={14} className="mr-2" /> : <EyeOff size={14} className="mr-2" />}
                                    {showHeatmap ? "On" : "Off"}
                                </Button>
                            </div>
                        </div>
                        <ImageViewer
                            src={data.imageUrl}
                            heatmapSrc={data.heatmapUrl}
                            heatmapOpacity={heatmapOpacity}
                            showHeatmap={showHeatmap}
                        />
                    </div>

                    {/* Module Score Chart */}
                    <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
                        <h3 className="font-semibold mb-6 flex items-center gap-2">
                            <BarChart2 size={18} className="text-primary" /> Confidence Impact Analysis
                        </h3>
                        <p className="text-xs text-muted-foreground mb-4">
                            Points deducted from Base 100 for each detected anomaly.
                        </p>
                        <div className="h-64 w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={moduleData} layout="vertical" margin={{ left: 40, right: 20 }}>
                                    <XAxis type="number" domain={[-60, 0]} hide={false} />
                                    <YAxis dataKey="name" type="category" width={140} tick={{ fontSize: 11 }} />
                                    <Tooltip
                                        formatter={(value) => [`${value} pts`, 'Penalty']}
                                        labelStyle={{ color: 'black' }}
                                        cursor={{ fill: 'transparent' }}
                                    />
                                    <CartesianGrid strokeDasharray="3 3" horizontal={false} strokeOpacity={0.3} />
                                    <Bar dataKey="score" fill="#ef4444" radius={[4, 0, 0, 4]} barSize={20}>
                                        {moduleData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.score < 0 ? '#ef4444' : '#e2e8f0'} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Right Col: Details */}
                <div className="space-y-6">
                    {/* Risk Gauge Card */}
                    <div className="bg-card border border-border rounded-xl p-6 shadow-sm flex flex-col items-center">
                        <h3 className="font-semibold text-sm text-muted-foreground mb-4 w-full">Confidence Score</h3>
                        <div className="w-48 h-24 relative">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={gaugeData}
                                        cy="100%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        startAngle={180}
                                        endAngle={0}
                                        paddingAngle={0}
                                        dataKey="value"
                                        stroke="none"
                                    >
                                        {gaugeData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                            <div className="absolute bottom-0 left-0 right-0 text-center">
                                <span className="text-3xl font-bold text-foreground">{(data.confidence_score * 100).toFixed(0)}%</span>
                            </div>
                        </div>
                        <p className="text-xs text-muted-foreground mt-2 text-center">
                            Risk Level: <span className="font-bold text-foreground">{data.module_reports?.raw?.risk_summary?.risk_level || "UNKNOWN"}</span>
                        </p>
                    </div>

                    {/* Extracted Data */}
                    <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
                        <h3 className="font-semibold mb-4 flex items-center gap-2">
                            <CheckCircle2 size={18} className="text-green-600" /> Extracted Data
                        </h3>
                        <div className="space-y-3 text-sm">
                            {/* We just show raw extracted fields for now, assuming BE provides flat dict */}
                            {Object.entries(data.extractedFields || {}).map(([key, value]) => (
                                <div key={key} className="flex justify-between border-b border-border pb-2 last:border-0 last:pb-0">
                                    <span className="text-muted-foreground capitalize">{key.replace(/_/g, ' ')}</span>
                                    <span className="font-medium text-right text-xs truncate max-w-[150px]" title={String(value)}>{String(value)}</span>
                                </div>
                            ))}
                            {Object.keys(data.extractedFields || {}).length === 0 && <p className="text-muted-foreground text-xs">No specific ID data extracted.</p>}
                        </div>
                    </div>

                    {/* Anomalies Card */}
                    <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
                        <h3 className="font-semibold mb-4 flex items-center gap-2">
                            <AlertCircle size={18} className="text-red-600" /> Detected Anomalies
                        </h3>
                        {data.anomalies && data.anomalies.length > 0 ? (
                            <div className="space-y-3">
                                {data.anomalies.map((anomaly, idx) => (
                                    <div key={idx} className="bg-destructive/5 border border-destructive/20 p-3 rounded-lg text-sm">
                                        <div className="flex justify-between items-start mb-2">
                                            <span className="bg-zinc-200 text-zinc-700 px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide">
                                                {anomaly.module_source?.replace('Module', '') || "SYSTEM"}
                                            </span>
                                        </div>
                                        <p className="font-medium text-destructive text-sm mb-1">{anomaly.description}</p>
                                        <div className="flex justify-between items-center mt-2 border-t border-destructive/10 pt-2">
                                            <span className="text-xs text-muted-foreground capitalize">{anomaly.region || 'General'}</span>
                                            {/* Ideally we'd show the impact score here if available in anomaly obj, but backend might not flatten it. Use generic score if > 0 */}
                                            {/* The risk engine puts aggregated impact on module, not individual anomaly. But we can infer if needed, or just leave it. */}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-sm text-muted-foreground">No anomalies detected.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
