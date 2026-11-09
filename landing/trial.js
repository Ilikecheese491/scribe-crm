// Scribe CRM tracking snippet — Lens taxonomy
// Replace API_URL with Render service URL, e.g. https://scribe.onrender.com
const API_URL = "https://scribe.onrender.com";
const PUBLIC_KEY = ""; // set via env on deploy, client sends empty by default

function uid(){ return Math.random().toString(36).slice(2)+Date.now().toString(36); }
function getKV(name, setIfMissing){
  const v = localStorage.getItem(name);
  if(v) return v;
  const nv = setIfMissing();
  localStorage.setItem(name, nv);
  return nv;
}
const session_id = getKV("scribe_session", () => uid());
const device_id = getKV("scribe_device", () => uid());

function parseUTM(){
  const p = new URLSearchParams(location.search);
  return {
    utm_source: p.get("utm_source")||"",
    utm_medium: p.get("utm_medium")||"",
    utm_campaign: p.get("utm_campaign")||""
  };
}
function post(event, extra={}){
  const body = {
    event_id: uid(),
    session_id,
    ts: Math.floor(Date.now()/1000),
    device: device_id,
    key: PUBLIC_KEY,
    product: "scribe",
    ...parseUTM(),
    ...extra
  };
  navigator.sendBeacon ? navigator.sendBeacon(API_URL+"/track", new Blob([JSON.stringify(body)],{type:"application/json"}))
  : fetch(API_URL+"/track", {method:"POST",body:JSON.stringify(body),headers:{"Content-Type":"application/json"},keepalive:true});
}
// session start on page load
post("session_start");

// CTA click helper
window.scribeTrack = (label, event_name) => post("cta_click", {channel:"web", event: event_name || label, cta_label: label});

// Demo view helper
window.scribeViewDemo = (demo_type) => post("demo_view", {demo_type});

// Trial start helper
window.scribeStartTrial = (email, businessSize) => post("trial_start", {email, business_size: businessSize});

// Activation helper — one per trial, client guards
let activated = localStorage.getItem("scribe_activated");
window.scribeActivate = (method) => {
  if(activated) return;
  post("activation", {method});
  localStorage.setItem("scribe_activated","1");
};
