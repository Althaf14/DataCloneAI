import React, { useState, useRef } from "react";
import { ZoomIn, ZoomOut, RotateCcw } from "lucide-react";
import { Button } from "../ui/Button";

export const ImageViewer = ({ src, heatmapSrc, heatmapOpacity = 0.5, showHeatmap = true }) => {
    const [scale, setScale] = useState(1);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

    const handleWheel = (e) => {
        // If ctrl key is pressed or just scroll? 
        // Usually map scroll to zoom in rich viewers
        if (e.ctrlKey || e.metaKey || true) {
            e.preventDefault();
            // Simple zoom logic
            const scaleAdjustment = -e.deltaY * 0.002;
            const newScale = Math.min(Math.max(0.5, scale + scaleAdjustment), 5);
            setScale(newScale);
        }
    };

    const handleMouseDown = (e) => {
        e.preventDefault();
        setIsDragging(true);
        setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
    };

    const handleMouseMove = (e) => {
        if (!isDragging) return;
        e.preventDefault();
        setPosition({
            x: e.clientX - dragStart.x,
            y: e.clientY - dragStart.y
        });
    };

    const handleMouseUp = () => setIsDragging(false);

    const reset = () => {
        setScale(1);
        setPosition({ x: 0, y: 0 });
    };

    return (
        <div className="relative w-full h-[600px] border border-border bg-slate-900/50 rounded-xl overflow-hidden group select-none">
            {/* Controls Overlay */}
            <div className="absolute top-4 right-4 z-20 flex flex-col gap-2 bg-background/90 backdrop-blur border border-border p-2 rounded-lg shadow-xl opacity-0 group-hover:opacity-100 transition-opacity">
                <Button variant="ghost" size="icon" onClick={() => setScale(s => Math.min(s + 0.5, 5))} title="Zoom In">
                    <ZoomIn size={18} />
                </Button>
                <Button variant="ghost" size="icon" onClick={() => setScale(s => Math.max(s - 0.5, 0.5))} title="Zoom Out">
                    <ZoomOut size={18} />
                </Button>
                <Button variant="ghost" size="icon" onClick={reset} title="Reset View">
                    <RotateCcw size={18} />
                </Button>
            </div>

            {/* Viewport */}
            <div
                className="w-full h-full flex items-center justify-center cursor-move overflow-hidden"
                onWheel={handleWheel}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
            >
                <div
                    style={{
                        transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
                        transition: isDragging ? 'none' : 'transform 0.15s cubic-bezier(0.2, 0, 0.3, 1)',
                        willChange: 'transform'
                    }}
                    className="relative inline-block shadow-2xl"
                >
                    {/* Base Image */}
                    <img
                        src={src}
                        alt="Document Base"
                        className="max-h-[500px] w-auto h-auto block rounded"
                        draggable={false}
                    />

                    {/* Heatmap Layer */}
                    {showHeatmap && heatmapSrc && (
                        <div
                            className="absolute inset-0 pointer-events-none mix-blend-multiply transition-opacity duration-300"
                            style={{
                                opacity: heatmapOpacity,
                                backgroundImage: `url(${heatmapSrc})`,
                                backgroundSize: 'cover'
                            }}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};
