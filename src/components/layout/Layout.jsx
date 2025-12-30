import React, { useState } from "react";
import { Outlet, Link } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Menu, Bell } from "lucide-react";
import { Button } from "../ui/Button";

export const Layout = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    return (
        <div className="min-h-screen bg-background flex">
            <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />

            <main className="flex-1 flex flex-col min-w-0">
                {/* Mobile Header */}
                <header className="md:hidden h-16 border-b border-border flex items-center px-4 justify-between bg-card">
                    <Button variant="ghost" size="icon" onClick={() => setIsSidebarOpen(true)}>
                        <Menu size={20} />
                    </Button>
                    <span className="font-bold">DataClone AI</span>
                    <div className="w-10" /> {/* Spacer */}
                </header>

                {/* Desktop Header / Toolbar (Optional) */}
                <header className="hidden md:flex h-16 border-b border-border items-center px-8 justify-end bg-card/50 backdrop-blur sticky top-0 z-30">
                    <Link to="/alerts">
                        <Button variant="ghost" size="icon" className="relative">
                            <Bell size={20} />
                            <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full" />
                        </Button>
                    </Link>
                </header>

                {/* Content Area */}
                <div className="flex-1 p-4 md:p-8 overflow-y-auto">
                    <div className="max-w-6xl mx-auto animate-in fade-in duration-500">
                        <Outlet />
                    </div>
                </div>
            </main>
        </div>
    );
};
