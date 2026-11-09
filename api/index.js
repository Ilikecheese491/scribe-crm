// Scribe Tracking API - Minimal Express server
const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());

// In-memory store (replace with DB in production)
const events = [];

app.post("/track", (req, res) => {
  const event = {
    received_at: new Date().toISOString(),
    ...req.body
  };
  events.push(event);
  console.log("Track event:", event.event, event.session_id);
  res.json({ ok: true, event_id: event.event_id });
});

app.get("/events", (req, res) => {
  res.json(events.slice(-100));
});

app.get("/health", (req, res) => {
  res.json({ status: "ok", events_count: events.length });
});

app.listen(PORT, () => {
  console.log(`Scribe Tracking API running on port ${PORT}`);
});
