import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { UploadCloud, FileText, ArrowRight, Activity } from "lucide-react";
import api from "../services/api";

export default function Dashboard() {
    const [stats, setStats] = useState({ today: 0, alerts: 0 });
    const [recentDocs, setRecentDocs] = useState([]);
    // Search & Filter State
    const [searchTerm, setSearchTerm] = useState("");
    const [filterType, setFilterType] = useState("all"); // 'all', 'id_proof', 'certificate'

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [docsRes, alertsRes] = await Promise.all([
                    api.get("/api/documents"),
                    api.get("/api/alerts")
                ]);

                const docs = docsRes.data || [];
                const alerts = alertsRes.data || [];

                // Calc today's docs
                const todayStr = new Date().toISOString().split('T')[0];
                const todayCount = docs.filter(d => d.upload_date && d.upload_date.startsWith(todayStr)).length;

                setStats({
                    today: todayCount,
                    alerts: alerts.length
                });

                setRecentDocs(docs); // Store all, filter locally
            } catch (e) {
                console.error("Dashboard fetch error", e);
            }
        };
        fetchData();
    }, []);

    // Derived state for filtered docs
    const filteredDocs = recentDocs.filter(doc => {
        const matchesSearch = doc.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
            doc.id.includes(searchTerm);
        const matchesType = filterType === "all" || (doc.doc_type === filterType);
        return matchesSearch && matchesType;
    });

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-muted-foreground">Overview of system activity and verification status.</p>
            </div>

            {/* Hero Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Quick Action: New Scan */}
                <Link to="/upload" className="group relative overflow-hidden rounded-xl border border-border bg-gradient-to-br from-primary to-primary/80 p-6 text-primary-foreground shadow-lg transition-transform hover:-translate-y-1">
                    <div className="relative z-10">
                        <h3 className="text-lg font-bold flex items-center gap-2">
                            <UploadCloud /> Start New Analysis
                        </h3>
                        <p className="mt-2 text-primary-foreground/90 text-sm">
                            Upload a document to detect forgery, heatmap anomalies, and duplicates.
                        </p>
                    </div>
                    <div className="absolute -bottom-4 -right-4 text-white/10 group-hover:scale-110 transition-transform">
                        <UploadCloud size={100} />
                    </div>
                </Link>

                {/* Stat 1 */}
                <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
                    <h3 className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                        <FileText size={16} /> Documents Processed Today
                    </h3>
                    <div className="mt-4 flex items-baseline gap-2">
                        <span className="text-3xl font-bold">{stats.today}</span>
                        <span className="text-sm text-muted-foreground">Updated just now</span>
                    </div>
                </div>

                {/* Stat 2 */}
                <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
                    <h3 className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                        <Activity size={16} /> Active Alerts
                    </h3>
                    <div className="mt-4 flex items-baseline gap-2">
                        <span className="text-3xl font-bold text-yellow-600">{stats.alerts}</span>
                        <span className="text-sm text-muted-foreground">Requires attention</span>
                    </div>
                </div>
            </div>

            {/* Recent Activity Section */}
            <div className="border border-border rounded-xl bg-card p-6">
                <div className="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
                    <h3 className="font-bold text-lg">Document History</h3>

                    {/* Search & Filter Controls */}
                    <div className="flex flex-col sm:flex-row gap-3">
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Search filename or ID..."
                                className="pl-3 pr-4 py-2 text-sm border border-input rounded-md bg-transparent w-full sm:w-64 focus:outline-none focus:ring-1 focus:ring-ring"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <select
                            className="px-3 py-2 text-sm border border-input rounded-md bg-transparent focus:outline-none focus:ring-1 focus:ring-ring"
                            value={filterType}
                            onChange={(e) => setFilterType(e.target.value)}
                        >
                            <option value="all">All Types</option>
                            <option value="id_proof">ID Proofs</option>
                            <option value="certificate">Certificates</option>
                        </select>
                        <Link to="/upload" className="text-sm bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md flex items-center gap-2 transition-colors">
                            New Upload <ArrowRight size={14} />
                        </Link>
                    </div>
                </div>

                <div className="rounded-md border overflow-hidden">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-muted/50 text-muted-foreground font-medium">
                            <tr>
                                <th className="px-4 py-3">Filename</th>
                                <th className="px-4 py-3">Type</th>
                                <th className="px-4 py-3">Date</th>
                                <th className="px-4 py-3">Status</th>
                                <th className="px-4 py-3 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {filteredDocs.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="px-4 py-8 text-center text-muted-foreground">
                                        No documents found matching your filters.
                                    </td>
                                </tr>
                            ) : (
                                filteredDocs.map((doc) => (
                                    <tr key={doc.id} className="hover:bg-accent/50 transition-colors group">
                                        <td className="px-4 py-3 font-medium">
                                            <div className="flex items-center gap-2">
                                                <FileText size={16} className="text-muted-foreground" />
                                                {doc.filename}
                                            </div>
                                        </td>
                                        <td className="px-4 py-3 capitalize">{doc.doc_type?.replace('_', ' ') || 'ID Proof'}</td>
                                        <td className="px-4 py-3 text-muted-foreground">{new Date(doc.upload_date).toLocaleDateString()}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${doc.status === 'verified' ? 'bg-green-100 text-green-700 border-green-200' :
                                                    doc.status === 'flagged' ? 'bg-red-100 text-red-700 border-red-200' :
                                                        'bg-yellow-100 text-yellow-700 border-yellow-200'
                                                }`}>
                                                {doc.status}
                                            </span>
                                        </td>
                                        <td className="px-4 py-3 text-right">
                                            <Link to={`/report/${doc.id}`} className="text-primary hover:underline opacity-0 group-hover:opacity-100 transition-opacity">
                                                View Report
                                            </Link>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
