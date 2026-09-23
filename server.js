const express = require("express");
// const cors = require("cors");

const app = express();

// app.use(cors());
app.use(express.json());

const PORT = 3000;

// Test route
app.get("/", (req, res) => {
    res.json({
        message: "Backend is running"
    });
});

// Model API
app.get("/api/predict", (req, res) => {
    const { animal, behaviour, intensity, abnormality_percentage, duration_minutes } = req.query;

    // Later you'll call your model here
    const result = {
        animal: animal,
        intensity: Number(intensity),
        prediction: "normal"
    };

    res.json(result);
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});