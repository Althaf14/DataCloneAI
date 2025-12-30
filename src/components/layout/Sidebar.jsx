import React from "react";
import { NavLink } from "react-router-dom";
import {
    LayoutDashboard,
    UploadCloud,
    FileText,
    LogOut,
    ShieldAlert,
    Menu
} from "lucide-react";
import { cn } from "../../utils/cn";
import { useAuth } from "../../context/AuthContext";

export const Sidebar = ({ isOpen, onClose }) => {
    const { logout } = useAuth();

    const navItems = [
        { to: "/", icon: LayoutDashboard, label: "Dashboard" },
        { to: "/upload", icon: UploadCloud, label: "New Analysis" },
        { to: "/alerts", icon: ShieldAlert, label: "Alerts" },
        // Only show Report if we had a specific ID, but here users can browse reports maybe?
        // Let's add a list view later. For now, link to a demo report.
        { to: "/report/demo", icon: FileText, label: "Demo Report" },
    ];

    return (
        <>
            {/* Mobile Overlay */}
            <div
                className={cn(
                    "fixed inset-0 bg-black/50 z-40 md:hidden transition-opacity",
                    isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
                )}
                onClick={onClose}
            />

            {/* Sidebar */}
            <div className={cn(
                "fixed md:sticky top-0 left-0 z-50 h-screen w-64 bg-card border-r border-border flex flex-col transition-transform duration-300 transform md:translate-x-0",
                isOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                {/* Header */}
                <div className="p-6 border-b border-border flex items-center gap-3">
                    <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                        <ShieldAlert className="text-primary-foreground w-5 h-5" />
                    </div>
                    <span className="font-bold text-xl tracking-tight">DataClone AI</span>
                </div>

                {/* Nav Links */}
                <nav className="flex-1 p-4 space-y-1">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            onClick={() => onClose && onClose()} // Close on mobile click
                            className={({ isActive }) => cn(
                                "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                                isActive
                                    ? "bg-primary/10 text-primary border border-primary/20"
                                    : "text-muted-foreground hover:bg-accent hover:text-foreground"
                            )}
                        >
                            <item.icon size={18} />
                            {item.label}
                        </NavLink>
                    ))}
                </nav>

                {/* Footer */}
                <div className="p-4 border-t border-border">
                    <button
                        onClick={logout}
                        className="flex items-center gap-3 w-full px-4 py-3 text-sm font-medium text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
                    >
                        <LogOut size={18} />
                        Sign Out
                    </button>
                </div>
            </div>
        </>
    );
};
