import React from "react";
import { cn } from "../../utils/cn";

export const Progress = ({ value = 0, className }) => {
    return (
        <div className={cn("relative h-4 w-full overflow-hidden rounded-full bg-secondary", className)}>
            <div
                className="h-full w-full flex-1 bg-primary transition-all duration-300 ease-in-out"
                style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
            />
        </div>
    );
};
