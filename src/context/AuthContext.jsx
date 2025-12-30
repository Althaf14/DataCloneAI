import React, { createContext, useContext, useState, useEffect } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check localStorage for persisted session
        try {
            const storedUser = localStorage.getItem("dc_user");
            if (storedUser) {
                setUser(JSON.parse(storedUser));
            }
        } catch (e) {
            console.error("Failed to parse user session", e);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const login = async (username, password) => {
        try {
            // FormData because OAuth2PasswordRequestForm in FastAPI expects form data
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const response = await api.post("/token", formData);
            if (response.data.access_token) {
                const u = {
                    name: username,
                    token: response.data.access_token,
                    // In a real app we might fetch user details here using the token
                    role: "admin"
                };
                setUser(u);
                localStorage.setItem("dc_user", JSON.stringify(u));
                return true;
            }
        } catch (error) {
            console.error("Login failed", error);
        }
        return false;
    };

    const register = async (username, password) => {
        try {
            const response = await api.post("/register", { username, password });
            if (response.data && response.data.id) {
                // Auto login after register
                return await login(username, password);
            }
        } catch (error) {
            console.error("Registration failed", error);
        }
        return false;
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem("dc_user");
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
