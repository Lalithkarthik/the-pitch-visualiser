/* ═══════════════════════════════════════════════════════
   PITCH VISUALIZER — script.js
   Full pipeline: generate → load → storyboard → download
   ═══════════════════════════════════════════════════════ */

'use strict';

// ─── State ───────────────────────────────────────────
let images   = [];
let captions = [];
let index    = 0;
let pipelineTimer = null;

// ─── DOM refs ─────────────────────────────────────────
const generateBtn      = document.getElementById('generateBtn');
const storyText        = document.getElementById('storyText');
const charCount        = document.getElementById('charCount');
const loadingOverlay   = document.getElementById('loadingOverlay');
const storyboardSec    = document.getElementById('storyboardSection');
const inputSection     = document.getElementById('inputSection');
const storyImage       = document.getElementById('storyImage');
const captionEl        = document.getElementById('captionText');
const panelBadge       = document.getElementById('panelBadge');
const prevBtn          = document.getElementById('prev');
const nextBtn          = document.getElementById('next');
const thumbnailStrip   = document.getElementById('thumbnailStrip');
const keyboardHint     = document.getElementById('keyboardHint');
const dlPdfBtn         = document.getElementById('dlPdfBtn');
const dlPptBtn         = document.getElementById('dlPptBtn');
const resetBtn         = document.getElementById('resetBtn');
const toast            = document.getElementById('toast');

// Pipeline step elements
const steps = [
  document.getElementById('step1'),
  document.getElementById('step2'),
  document.getElementById('step3'),
  document.getElementById('step4'),
  document.getElementById('step5'),
];

// Step timing in ms (approximate pipeline durations)
const STEP_DURATIONS = [600, 2400, 1800, 6000, 1200];

// ─── Character counter ────────────────────────────────
storyText.addEventListener('input', () => {
  const n = storyText.value.length;
  charCount.textContent = n.toLocaleString() + ' character' + (n !== 1 ? 's' : '');
});

// ─── Generate ─────────────────────────────────────────
generateBtn.addEventListener('click', async () => {
  const text = storyText.value.trim();
  if (!text) {
    showToast('Please paste your story first.', 'error');
    storyText.focus();
    return;
  }

  const styleEl = document.querySelector('input[name="style"]:checked');
  const style   = styleEl ? styleEl.value : null;

  startLoading();

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, style }),
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const data = await response.json();

    images   = data.images   || [];
    captions = data.captions || [];
    index    = 0;

    if (!images.length) throw new Error('No images returned from server.');

    stopLoading();
    showStoryboard();

  } catch (err) {
    console.error('Generation failed:', err);
    stopLoading();
    showToast('Something went wrong. Please try again.', 'error');
    generateBtn.disabled = false;
  }
});

// ─── Loading state ────────────────────────────────────
function startLoading() {
  generateBtn.disabled = true;
  loadingOverlay.setAttribute('aria-hidden', 'false');
  loadingOverlay.classList.add('active');

  // Reset steps
  steps.forEach(s => s.classList.remove('active', 'done'));

  // Animate pipeline steps
  let elapsed = 0;
  let stepIndex = 0;

  function advanceStep() {
    if (stepIndex >= steps.length) return;

    // Mark previous done
    if (stepIndex > 0) steps[stepIndex - 1].classList.remove('active');
    if (stepIndex > 0) steps[stepIndex - 1].classList.add('done');

    steps[stepIndex].classList.add('active');
    stepIndex++;

    if (stepIndex < steps.length) {
      pipelineTimer = setTimeout(advanceStep, STEP_DURATIONS[stepIndex - 1]);
    }
  }

  advanceStep();
}

function stopLoading() {
  if (pipelineTimer) clearTimeout(pipelineTimer);

  // Quickly complete all steps
  steps.forEach(s => { s.classList.remove('active'); s.classList.add('done'); });

  setTimeout(() => {
    loadingOverlay.classList.remove('active');
    loadingOverlay.setAttribute('aria-hidden', 'true');
    generateBtn.disabled = false;
  }, 400);
}

// ─── Show storyboard ─────────────────────────────────
function showStoryboard() {
  inputSection.style.display  = 'none';
  storyboardSec.classList.add('visible');

  buildThumbnails();
  renderPanel(index, false);
}

// ─── Render a panel ───────────────────────────────────
function renderPanel(i, animate = true) {
  const img = storyImage;
  const cap = captionEl;

  if (animate) {
    img.classList.add('fading');
    cap.classList.add('fading');
  }

  const finalize = () => {
    img.src = images[i];
    cap.textContent = captions[i] || '';
    panelBadge.textContent = `PANEL ${pad(i + 1)} / ${pad(images.length)}`;

    // Update nav arrows visibility
    prevBtn.hidden = images.length <= 1;
    nextBtn.hidden = images.length <= 1;
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === images.length - 1;

    // Update thumbnails
    document.querySelectorAll('.thumb').forEach((t, ti) => {
      t.classList.toggle('active', ti === i);
    });

    if (animate) {
      img.classList.remove('fading');
      cap.classList.remove('fading');
    }
  };

  if (animate) {
    setTimeout(finalize, 300);
  } else {
    finalize();
  }
}

function pad(n) {
  return String(n).padStart(2, '0');
}

// ─── Build thumbnails ─────────────────────────────────
function buildThumbnails() {
  thumbnailStrip.innerHTML = '';

  images.forEach((src, i) => {
    const thumb = document.createElement('div');
    thumb.className = 'thumb' + (i === 0 ? ' active' : '');
    thumb.setAttribute('role', 'tab');
    thumb.setAttribute('aria-label', `Panel ${i + 1}`);
    thumb.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
    thumb.tabIndex = 0;

    const img = document.createElement('img');
    img.src = src;
    img.alt = `Panel ${i + 1}`;
    img.loading = 'lazy';

    const num = document.createElement('span');
    num.className = 'thumb-num';
    num.textContent = pad(i + 1);

    thumb.appendChild(img);
    thumb.appendChild(num);
    thumbnailStrip.appendChild(thumb);

    thumb.addEventListener('click', () => goTo(i));
    thumb.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') goTo(i);
    });
  });

  // Show keyboard hint only if multiple panels
  keyboardHint.style.display = images.length > 1 ? 'flex' : 'none';
}

// ─── Navigation ───────────────────────────────────────
function goTo(i) {
  if (i < 0 || i >= images.length || i === index) return;
  index = i;
  renderPanel(index, true);
}

prevBtn.addEventListener('click', () => goTo(index - 1));
nextBtn.addEventListener('click', () => goTo(index + 1));

document.addEventListener('keydown', e => {
  if (!storyboardSec.classList.contains('visible')) return;
  if (e.key === 'ArrowRight') goTo(index + 1);
  if (e.key === 'ArrowLeft')  goTo(index - 1);
});

// ─── Reset / New Story ───────────────────────────────
resetBtn.addEventListener('click', () => {
  images   = [];
  captions = [];
  index    = 0;

  storyboardSec.classList.remove('visible');
  inputSection.style.display = '';
  storyText.value = '';
  charCount.textContent = '0 characters';

  window.scrollTo({ top: 0, behavior: 'smooth' });
  storyText.focus();
});

// ─── Image to base64 helper ──────────────────────────
async function fetchImageAsBase64(src) {
  const res  = await fetch(src);
  const blob = await res.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.onerror  = reject;
    reader.readAsDataURL(blob);
  });
}

// ─── Download PDF ─────────────────────────────────────
dlPdfBtn.addEventListener('click', async () => {
  if (!images.length) return;
  dlPdfBtn.classList.add('loading');
  dlPdfBtn.querySelector('span:last-child').textContent = 'Building PDF…';

  try {
    const { jsPDF } = window.jspdf;

    // 16:9 page at 96dpi
    const W = 297, H = 167.06; // mm landscape A4-ish 16:9
    const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: [W, H + 20] });

    for (let i = 0; i < images.length; i++) {
      if (i > 0) pdf.addPage();

      const imgData = await fetchImageAsBase64(images[i]);
      pdf.addImage(imgData, 'JPEG', 0, 0, W, H);

      // Dark footer band
      pdf.setFillColor(7, 7, 13);
      pdf.rect(0, H, W, 20, 'F');

      // Caption
      pdf.setFont('helvetica', 'italic');
      pdf.setFontSize(9);
      pdf.setTextColor(220, 215, 200);
      const cap = captions[i] || '';
      pdf.text(cap, W / 2, H + 12, { align: 'center', maxWidth: W - 20 });

      // Panel number (top-left)
      pdf.setFontSize(7);
      pdf.setTextColor(150, 140, 120);
      pdf.text(`${pad(i + 1)} / ${pad(images.length)}`, 6, 8);
    }

    pdf.save('storyboard.pdf');
    showToast('PDF exported successfully.', 'success');

  } catch (err) {
    console.error('PDF export failed:', err);
    showToast('PDF export failed. Try again.', 'error');
  } finally {
    dlPdfBtn.classList.remove('loading');
    dlPdfBtn.querySelector('span:last-child').textContent = 'Export PDF';
  }
});

// ─── Download PPT ─────────────────────────────────────
dlPptBtn.addEventListener('click', async () => {
  if (!images.length) return;
  dlPptBtn.classList.add('loading');
  dlPptBtn.querySelector('span:last-child').textContent = 'Building PPT…';

  try {
    const pptx = new PptxGenJS();
    pptx.layout = 'LAYOUT_16x9';
    pptx.defineLayout({ name: 'LAYOUT_16x9', width: 10, height: 5.625 });

    for (let i = 0; i < images.length; i++) {
      const slide = pptx.addSlide();

      // Background
      slide.background = { color: '07070D' };

      // Image
      const imgData = await fetchImageAsBase64(images[i]);
      const base64  = imgData.split(',')[1];
      const ext     = imgData.includes('image/png') ? 'png' : 'jpg';

      slide.addImage({
        data: `${ext};base64,${base64}`,
        x: 0, y: 0,
        w: 10, h: 4.8,
      });

      // Caption band
      slide.addShape(pptx.ShapeType.rect, {
        x: 0, y: 4.8, w: 10, h: 0.825,
        fill: { color: '0F0F1C' },
        line:  { color: '1F1F35', width: 1 },
      });

      // Caption text
      const cap = captions[i] || '';
      slide.addText(cap, {
        x: 0.3, y: 4.85, w: 9.4, h: 0.7,
        fontSize: 14,
        fontFace: 'Georgia',
        italic: true,
        color: 'ECE9E2',
        align: 'center',
        valign: 'middle',
      });

      // Panel number badge
      slide.addText(`${pad(i + 1)} / ${pad(images.length)}`, {
        x: 0.15, y: 0.1, w: 0.9, h: 0.28,
        fontSize: 8,
        fontFace: 'Courier New',
        color: 'C9A84C',
        fill: { color: '0F0F1C', transparency: 30 },
        align: 'center',
      });
    }

    await pptx.writeFile({ fileName: 'storyboard.pptx' });
    showToast('PPT exported successfully.', 'success');

  } catch (err) {
    console.error('PPT export failed:', err);
    showToast('PPT export failed. Try again.', 'error');
  } finally {
    dlPptBtn.classList.remove('loading');
    dlPptBtn.querySelector('span:last-child').textContent = 'Export PPT';
  }
});

// ─── Toast ────────────────────────────────────────────
let toastTimer = null;

function showToast(msg, type = '') {
  toast.textContent = msg;
  toast.className = 'toast show' + (type ? ' ' + type : '');

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove('show');
  }, 3200);
}