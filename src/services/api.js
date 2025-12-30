import axios from "axios";

// Toggle Mock Mode here
export const MOCK_MODE = false;

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 10000,
});

// Request interceptor to add token
api.interceptors.request.use(
    (config) => {
        const userStr = localStorage.getItem("dc_user");
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                if (user.token) {
                    config.headers.Authorization = `Bearer ${user.token}`;
                }
            } catch (e) {
                console.error("Error parsing user token", e);
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle 401s
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Token expired or invalid
            localStorage.removeItem("dc_user");
            // Force redirect to login if we can't access history/navigate here easily
            // Note: This is a harsh redirect, but effective for cleaning bad state
            if (!window.location.pathname.includes("/login")) {
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

/* --- Mock Data --- */
// ... existing mock data code kept but unused if MOCK_MODE is false ...
const MOCK_ALERTS = [
    { id: 1, type: "forgery", severity: "high", message: "Duplicate ID #9928 Detected", timestamp: "10 mins ago" },
    { id: 2, type: "manipulation", severity: "medium", message: "Pixel inconsistencies in photo region", timestamp: "2 hours ago" },
    { id: 3, type: "system", severity: "low", message: "System maintenance scheduled", timestamp: "1 day ago" },
];

const MOCK_REPORT = {
    id: "doc-mock-1",
    status: "flagged",
    confidence: 0.98,
    heatmapUrl: "https://placehold.co/800x600/png?text=Heatmap+Overlay&font=roboto",
    imageUrl: "https://placehold.co/800x600/png?text=Document+Image&font=roboto",
    extractedFields: {
        fullName: "ALI KHAN",
        documentNumber: "A12345678",
        dob: "15/05/1985",
        expiryDate: "14/05/2030"
    },
    anomalies: [
        { region: "photo", score: 0.95, description: "Synthetic face patterns detected" },
        { region: "text_name", score: 0.88, description: "Font weight inconsistency" }
    ]
};

// Custom Adapter for Mocking
const mockAdapter = async (config) => {
    console.log(`[Mock API] Request: ${config.method.toUpperCase()} ${config.url}`);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));

    const { url, method } = config;

    // Login (Handled by AuthContext mostly, but if we had server auth)
    if (url === '/auth/login' && method === 'post') {
        return { status: 200, data: { token: "mock-jwt" } };
    }

    // Upload
    if (url.includes('/documents/upload') && method === 'post') {
        return { status: 200, data: { id: "doc-mock-1", message: "Upload successful" } };
    }

    // Document Report
    if (url.match(/\/documents\/.*\/report/) && method === 'get') {
        return { status: 200, data: MOCK_REPORT };
    }

    // Alerts
    if (url.includes('/alerts') && method === 'get') {
        return { status: 200, data: MOCK_ALERTS };
    }

    // Document details
    if (url.match(/\/documents\/.*/) && method === 'get') {
        return { status: 200, data: { id: "doc-mock-1", status: "processed" } };
    }

    return { status: 404, data: { message: "Mock Route Not Found" } };
};

if (MOCK_MODE) {
    api.defaults.adapter = mockAdapter;
}

export default api;
