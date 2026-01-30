/* Frontend interaction for the demo dashboard
   - Sends an image to /analyze (multipart form) or uses bundled sample
   - Renders detections, SOP mappings and annotated image
*/

const el = id => document.getElementById(id);
const preview = el('preview');
const overlay = el('overlay');
const fileInput = el('file');
const runBtn = el('run');
const runSampleBtn = el('run-sample');
const spinner = el('spinner');
const errorEl = el('error');
const resultsEl = el('results');
const severityEl = el('severity');
const metaEl = el('meta');
const annotatedImg = el('annotated');
const statusEl = el('service-status');

// Check service health on load
fetch('/health').then(r => r.json()).then(j => {
  statusEl.textContent = `Service: ${j.status} — v${j.version}`;
}).catch(()=>{statusEl.textContent='Service: unreachable';statusEl.style.opacity=.6});

// Keep canvas size in sync with preview
function fitCanvas(){
  overlay.width = preview.clientWidth;
  overlay.height = preview.clientHeight;
}
window.addEventListener('resize', fitCanvas);
preview.addEventListener('load', fitCanvas);

fileInput.addEventListener('change', e => {
  const f = e.target.files && e.target.files[0];
  if (!f) return;
  preview.src = URL.createObjectURL(f);
  annotatedImg.src = '';
  clearResults();
});

runBtn.addEventListener('click', () => runInspection(false));
runSampleBtn.addEventListener('click', () => runInspection(true));

function setBusy(b){
  spinner.classList.toggle('hidden', !b);
  runBtn.disabled = b;
  runSampleBtn.disabled = b;
}

function clearResults(){
  resultsEl.innerHTML = '<em>No results — run an inspection to see detections, SOP mappings and recommendations.</em>';
  severityEl.textContent = '—';
  severityEl.className = 'badge';
  annotatedImg.src = '';
  const ctx = overlay.getContext('2d'); ctx && ctx.clearRect(0,0,overlay.width,overlay.height);
}

async function runInspection(useSample){
  errorEl.textContent = '';
  setBusy(true);
  clearResults();

  try{
    const fd = new FormData();
    if (useSample || !fileInput.files.length){
      // tell API to use the server-side sample image
      const resp = await fetch('/analyze', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({use_sample:true})});
      await handleResponse(resp);
      return;
    }

    fd.append('image', fileInput.files[0]);
    const resp = await fetch('/analyze', {method:'POST', body: fd});
    await handleResponse(resp);
  }catch(err){
    errorEl.textContent = err.message || String(err);
  }finally{setBusy(false)}
}

async function handleResponse(resp){
  if (!resp.ok){
    const txt = await resp.text();
    errorEl.textContent = `Server error: ${txt}`;
    return;
  }
  const j = await resp.json();
  renderResults(j);
}

function renderResults(payload){
  if (payload.error){ errorEl.textContent = payload.error; return; }

  const det = payload.detections || [];
  const analysis = payload.analysis || {};

  // Summary
  const sev = analysis.severity || 'low';
  severityEl.textContent = sev.toUpperCase();
  severityEl.className = `badge ${sev}`;
  metaEl.textContent = `Detected: ${analysis.summary ? analysis.summary.total : det.length} defect(s)`;

  // Results list
  if (!det.length){
    resultsEl.innerHTML = '<em>No defects found.</em>';
  } else {
    resultsEl.innerHTML = det.map(d=>{
      const lbl = d.label;
      const conf = (d.confidence||0).toFixed(2);
      return `<div class="result-item"><div style="width:8px;height:8px;border-radius:4px;background:#fff;margin-top:6px"></div><div><b>${lbl} — ${conf}</b><div>bbox: ${d.bbox.join(', ')}</div></div></div>`;
    }).join('');

    // SOPs & recommendations
    const sops = (analysis.sop_mappings||[]).map(s=>`<li><b>${s.label}</b> — ${s.iso} — ${s.sop} (priority ${s.priority})</li>`).join('');
    const recs = (analysis.recommendations||[]).map(r=>`<li>${r}</li>`).join('');
    resultsEl.insertAdjacentHTML('beforeend', `<h4 style="margin-top:10px">SOP / ISO</h4><ul>${sops}</ul><h4>Recommendations</h4><ul>${recs}</ul>`);
  }

  // Annotated image
  if (payload.annotated_image){
    annotatedImg.src = payload.annotated_image;
  }

  // Draw overlay on original preview for interactivity
  drawOverlay(det);
}

function drawOverlay(detections){
  const ctx = overlay.getContext('2d');
  if (!ctx) return;
  ctx.clearRect(0,0,overlay.width,overlay.height);
  if (!detections.length) return;

  const img = preview;
  const sw = img.naturalWidth || img.width;
  const sh = img.naturalHeight || img.height;
  const dw = preview.clientWidth;
  const dh = preview.clientHeight;
  const sx = dw / sw, sy = dh / sh; // scale

  detections.forEach(d => {
    const [x,y,w,h] = d.bbox;
    ctx.strokeStyle = d.label === 'leak' ? 'rgba(255,80,80,0.95)' : 'rgba(255,200,0,0.95)';
    ctx.lineWidth = 3;
    ctx.strokeRect(x * sx, y * sy, w * sx, h * sy);
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.fillRect(x * sx, y * sy - 22, ctx.measureText(d.label).width + 24, 20);
    ctx.fillStyle = '#fff';
    ctx.fillText(`${d.label} ${d.confidence.toFixed(2)}`, x * sx + 6, y * sy - 6);
  });
}

// initialize
fitCanvas();
clearResults();
