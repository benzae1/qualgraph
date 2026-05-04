const state = {
  summary: null,
  clusters: [],
  findings: [],
  graph: null,
  mode: 'clusters',
  activeCluster: null,
  activeNode: null,
  activeSource: '',
  query: '',
  particles: [],
  hover: null,
  selected: null,
  needsFit: true,
  viewport: { x: 0, y: 0, scale: 1 },
  pointer: { dragging: false, moved: false, lastX: 0, lastY: 0 }
};

const els = {
  canvas: document.getElementById('graphCanvas'),
  graphPath: document.getElementById('graphPath'),
  summaryGrid: document.getElementById('summaryGrid'),
  clusterList: document.getElementById('clusterList'),
  findingsList: document.getElementById('findingsList'),
  findingsTitle: document.getElementById('findingsTitle'),
  findingCount: document.getElementById('findingCount'),
  inspector: document.getElementById('inspectorPanel'),
  search: document.getElementById('searchInput'),
  modeLabel: document.getElementById('modeLabel'),
  viewTitle: document.getElementById('viewTitle')
};

const ctx = els.canvas.getContext('2d');
let width = 0;
let height = 0;
let frame = 0;

async function boot() {
  const [summary, clusters, graph, findings] = await Promise.all([
    fetchJson('/api/summary'),
    fetchJson('/api/clusters'),
    fetchJson('/api/graph'),
    fetchJson('/api/findings')
  ]);
  state.summary = summary;
  state.clusters = clusters.clusters;
  state.graph = graph;
  state.findings = findings.findings;
  setOverviewModeLabel();
  renderSummary();
  renderClusters();
  renderFindings();
  renderEmpty();
  resize();
  requestAnimationFrame(tick);
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url}: ${response.status}`);
  return response.json();
}

function renderSummary() {
  els.graphPath.textContent = state.summary.graph_path || 'Graph artifact';
  const metrics = [
    ['Nodes', state.summary.nodes],
    ['Edges', state.summary.edges],
    ['Clusters', state.summary.clusters],
    ['Findings', state.summary.findings],
    ['LLM', state.summary.llm_findings],
    ['Warnings', state.summary.warnings.length]
  ];
  els.summaryGrid.innerHTML = metrics.map(([label, value]) => `
    <div class="metric"><strong>${fmt(value)}</strong><span>${label}</span></div>
  `).join('');
}

function renderClusters() {
  const query = state.query.toLowerCase();
  const clusters = state.clusters.filter(cluster => !query || cluster.name.toLowerCase().includes(query));
  els.clusterList.innerHTML = clusters.slice(0, 80).map(cluster => `
    <div class="row ${state.activeCluster === cluster.id ? 'is-active' : ''}" data-cluster="${escapeAttr(cluster.id)}">
      <strong>${escapeHtml(cluster.name)}</strong>
      <small>${cluster.size} nodes · ${cluster.finding_count} findings · max risk ${cluster.max_risk_score.toFixed(1)}</small>
    </div>
  `).join('');
}

function renderFindings(source = state.activeSource) {
  state.activeSource = source;
  const query = state.query.toLowerCase();
  let findings = state.findings;
  if (source) findings = findings.filter(item => item.source === source);
  if (query) {
    findings = findings.filter(item => [
      item.node_name, item.file_path, item.message, item.code, item.source
    ].join(' ').toLowerCase().includes(query));
  }
  els.findingsTitle.textContent = source === 'llm' ? 'LLM Findings' : 'Findings';
  els.findingCount.textContent = findings.length;
  els.findingsList.innerHTML = findings.slice(0, 100).map(item => `
    <div class="finding-card" data-node="${escapeAttr(item.node_id)}">
      <span class="badge sev-${escapeAttr(item.severity)}">${escapeHtml(item.severity)}</span>
      <span class="badge">${escapeHtml(item.source)} ${escapeHtml(item.code)}</span>
      <strong>${escapeHtml(item.node_name)}</strong>
      <p>${escapeHtml(item.message)}</p>
    </div>
  `).join('');
}

function renderEmpty() {
  els.inspector.innerHTML = `
    <div class="empty">
      <span class="pulse"></span>
      <h2>Select a cluster or node</h2>
      <p>Drill through the graph to inspect findings, risk signals, source evidence, and relationships.</p>
    </div>
  `;
}

function renderCluster(cluster) {
  els.inspector.innerHTML = `
    <h2>${escapeHtml(cluster.name)}</h2>
    <div class="kv">
      <div><span>Nodes</span><strong>${fmt(cluster.size)}</strong></div>
      <div><span>Findings</span><strong>${fmt(cluster.finding_count)}</strong></div>
      <div><span>LLM Findings</span><strong>${fmt(cluster.llm_finding_count)}</strong></div>
      <div><span>Max Risk</span><strong>${cluster.max_risk_score.toFixed(2)}</strong></div>
    </div>
    <h3>Top Risk Nodes</h3>
    <div class="list">
      ${cluster.top_risk_nodes.map(node => `
        <div class="row" data-node="${escapeAttr(node.id)}">
          <strong>${escapeHtml(node.qualified_name)}</strong>
          <small>${escapeHtml(node.file_path || '')}:${node.line_start || ''} · risk ${node.risk_score.toFixed(1)}</small>
        </div>
      `).join('') || '<p class="muted">No risk nodes in this cluster.</p>'}
    </div>
  `;
}

async function renderNode(nodeId) {
  const node = await fetchJson(`/api/node?id=${encodeURIComponent(nodeId)}`);
  state.activeNode = node.id;
  els.inspector.innerHTML = `
    <h2>${escapeHtml(node.qualified_name)}</h2>
    <p class="muted">${escapeHtml(node.file_path || '')}:${node.line_start || ''}-${node.line_end || ''}</p>
    <div class="kv">
      <div><span>Risk</span><strong>${node.risk_score.toFixed(2)}</strong></div>
      <div><span>Findings</span><strong>${node.finding_count}</strong></div>
      <div><span>Complexity</span><strong>${node.complexity ?? 'n/a'}</strong></div>
      <div><span>Churn</span><strong>${node.churn ?? 0}</strong></div>
    </div>
    <h3>Findings</h3>
    <div class="list">${node.findings.map(findingCard).join('') || '<p class="muted">No findings on this node.</p>'}</div>
    <h3>Risk Components</h3>
    <div>${Object.entries(node.risk_components || {}).map(([k, v]) => `<span class="badge">${escapeHtml(k)}=${Number(v).toFixed(2)}</span>`).join('') || '<span class="badge">none</span>'}</div>
    <h3>Source</h3>
    <pre class="source">${escapeHtml(node.source || 'No source snippet stored in graph.')}</pre>
    <h3>Relationships</h3>
    <div class="list">${[...node.relationships.outgoing, ...node.relationships.incoming].slice(0, 20).map(rel => `
      <div class="row" data-node="${escapeAttr(rel.id)}">
        <strong>${escapeHtml(rel.qualified_name)}</strong>
        <small>${escapeHtml(rel.direction)} · ${escapeHtml(rel.edge_type)} · ${escapeHtml(rel.file_path || '')}</small>
      </div>
    `).join('') || '<p class="muted">No relationships.</p>'}</div>
  `;
}

function findingCard(item) {
  return `
    <div class="finding-card">
      <span class="badge sev-${escapeAttr(item.severity)}">${escapeHtml(item.severity)}</span>
      <span class="badge">${escapeHtml(item.source)} ${escapeHtml(item.code)}</span>
      <p>${escapeHtml(item.message || '')}</p>
      ${item.evidence ? `<p><strong>Evidence:</strong> ${escapeHtml(String(item.evidence))}</p>` : ''}
      ${item.suggested_action ? `<p><strong>Action:</strong> ${escapeHtml(item.suggested_action)}</p>` : ''}
    </div>
  `;
}

async function drillCluster(clusterId) {
  state.activeCluster = clusterId;
  state.activeNode = null;
  state.mode = 'cluster';
  state.graph = await fetchJson(`/api/graph?cluster=${encodeURIComponent(clusterId)}`);
  state.needsFit = true;
  state.viewport = { x: 0, y: 0, scale: 1 };
  const cluster = state.clusters.find(item => item.id === clusterId);
  els.modeLabel.textContent = 'Cluster Detail';
  els.viewTitle.textContent = cluster ? cluster.name : `Cluster ${clusterId}`;
  renderClusters();
  if (cluster) renderCluster(cluster);
}

async function overview() {
  state.activeCluster = null;
  state.activeNode = null;
  state.mode = 'clusters';
  state.graph = await fetchJson('/api/graph');
  state.needsFit = true;
  state.viewport = { x: 0, y: 0, scale: 1 };
  setOverviewModeLabel();
  els.viewTitle.textContent = 'System overview';
  renderClusters();
  renderEmpty();
}

function resize() {
  const rect = els.canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  width = rect.width;
  height = rect.height;
  els.canvas.width = Math.max(1, Math.floor(width * dpr));
  els.canvas.height = Math.max(1, Math.floor(height * dpr));
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  state.needsFit = true;
}

function seedPositions() {
  const nodes = state.graph.nodes || [];
  const radius = Math.min(width, height) * 0.32;
  nodes.forEach((node, i) => {
    if (node.x !== undefined && !state.needsFit) return;
    const angle = (Math.PI * 2 * i) / Math.max(nodes.length, 1);
    const jitter = 0.82 + ((i * 37) % 23) / 100;
    node.x = width / 2 + Math.cos(angle) * radius * jitter;
    node.y = height / 2 + Math.sin(angle) * radius * jitter;
    node.vx = 0;
    node.vy = 0;
  });
  if (state.viewport.scale === 1 && state.viewport.x === 0 && state.viewport.y === 0) {
    state.viewport.x = 0;
    state.viewport.y = 0;
  }
  state.needsFit = false;
}

function simulate() {
  const nodes = state.graph.nodes || [];
  const edges = state.graph.edges || [];
  const byId = new Map(nodes.map(node => [node.id, node]));
  for (const node of nodes) {
    node.vx += (width / 2 - node.x) * 0.0009;
    node.vy += (height / 2 - node.y) * 0.0009;
  }
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      const dx = b.x - a.x, dy = b.y - a.y;
      const d2 = Math.max(80, dx * dx + dy * dy);
      const force = Math.min(1.9, 4200 / d2);
      const d = Math.sqrt(d2);
      a.vx -= dx / d * force; a.vy -= dy / d * force;
      b.vx += dx / d * force; b.vy += dy / d * force;
    }
  }
  for (const edge of edges) {
    const a = byId.get(edge.source), b = byId.get(edge.target);
    if (!a || !b) continue;
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.max(1, Math.sqrt(dx * dx + dy * dy));
    const target = state.mode === 'clusters' ? 190 : 120;
    const force = (d - target) * 0.004;
    a.vx += dx / d * force; a.vy += dy / d * force;
    b.vx -= dx / d * force; b.vy -= dy / d * force;
  }
  for (const node of nodes) {
    node.vx *= 0.84;
    node.vy *= 0.84;
    node.x += node.vx;
    node.y += node.vy;
  }
}

function draw() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = '#080a0f';
  ctx.fillRect(0, 0, width, height);
  const nodes = state.graph.nodes || [];
  const edges = state.graph.edges || [];
  const byId = new Map(nodes.map(node => [node.id, node]));
  const labelSet = labelCandidates(nodes);
  ctx.save();
  ctx.translate(state.viewport.x, state.viewport.y);
  ctx.scale(state.viewport.scale, state.viewport.scale);
  ctx.globalAlpha = 0.55;
  for (const edge of edges) {
    const a = byId.get(edge.source), b = byId.get(edge.target);
    if (!a || !b) continue;
    ctx.strokeStyle = edge.type === 'tested_by' ? 'rgba(88,97,116,.28)' : 'rgba(112,167,255,.22)';
    ctx.lineWidth = Math.min(4, Math.max(1, Math.log(edge.weight || 1)));
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }
  ctx.restore();
  ctx.save();
  ctx.translate(state.viewport.x, state.viewport.y);
  ctx.scale(state.viewport.scale, state.viewport.scale);
  for (const node of nodes) {
    const r = nodeRadius(node);
    const active = state.selected === node.id || state.activeNode === node.id || state.activeCluster === node.id;
    ctx.beginPath();
    ctx.fillStyle = nodeColor(node);
    ctx.shadowColor = active ? '#58e6d9' : nodeColor(node);
    ctx.shadowBlur = active ? 28 : 10;
    ctx.arc(node.x, node.y, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    if (node.finding_count || node.llm_finding_count) {
      ctx.strokeStyle = node.llm_finding_count ? '#f2b866' : 'rgba(242,184,102,.65)';
      ctx.lineWidth = 2;
      ctx.stroke();
    }
    if (active || labelSet.has(node.id)) {
      ctx.fillStyle = '#dfe8ff';
      ctx.font = `${Math.max(10, 12 / Math.sqrt(state.viewport.scale))}px Segoe UI`;
      ctx.textAlign = 'center';
      ctx.fillText(trim(node.label || node.name || node.qualified_name, 28), node.x, node.y + r + 15);
    }
  }
  ctx.restore();
}

function tick() {
  frame++;
  if (state.graph) {
    seedPositions();
    for (let i = 0; i < 2; i++) simulate();
    draw();
  }
  requestAnimationFrame(tick);
}

function nodeRadius(node) {
  if (state.mode === 'clusters') return 9 + Math.sqrt(node.size || 1) * 1.2 + Math.min(12, node.finding_count || 0);
  return 6 + Math.min(14, Math.max(0, node.risk_score || 0) * 2.4) + Math.min(4, node.finding_count || 0);
}

function nodeColor(node) {
  if (node.llm_finding_count) return '#f2b866';
  if (node.finding_count) return '#70a7ff';
  if (node.kind === 'test' || node.is_test) return '#586174';
  return '#58e6d9';
}

function pickNode(x, y) {
  const point = screenToWorld(x, y);
  const nodes = [...(state.graph.nodes || [])].reverse();
  return nodes.find(node => {
    const dx = point.x - node.x, dy = point.y - node.y;
    return Math.sqrt(dx * dx + dy * dy) <= nodeRadius(node) + 4;
  });
}

els.canvas.addEventListener('click', async event => {
  if (state.pointer.moved) return;
  const rect = els.canvas.getBoundingClientRect();
  const node = pickNode(event.clientX - rect.left, event.clientY - rect.top);
  if (!node) return;
  state.selected = node.id;
  if (state.mode === 'clusters') await drillCluster(node.id);
  else await renderNode(node.id);
});

els.canvas.addEventListener('pointerdown', event => {
  els.canvas.setPointerCapture(event.pointerId);
  state.pointer.dragging = true;
  state.pointer.moved = false;
  state.pointer.lastX = event.clientX;
  state.pointer.lastY = event.clientY;
});

els.canvas.addEventListener('pointermove', event => {
  if (!state.pointer.dragging) return;
  const dx = event.clientX - state.pointer.lastX;
  const dy = event.clientY - state.pointer.lastY;
  if (Math.abs(dx) + Math.abs(dy) > 2) state.pointer.moved = true;
  state.viewport.x += dx;
  state.viewport.y += dy;
  state.pointer.lastX = event.clientX;
  state.pointer.lastY = event.clientY;
});

els.canvas.addEventListener('pointerup', event => {
  state.pointer.dragging = false;
  try {
    els.canvas.releasePointerCapture(event.pointerId);
  } catch {
    // Pointer capture can already be released by the browser.
  }
  setTimeout(() => { state.pointer.moved = false; }, 0);
});

els.canvas.addEventListener('wheel', event => {
  event.preventDefault();
  const rect = els.canvas.getBoundingClientRect();
  const before = screenToWorld(event.clientX - rect.left, event.clientY - rect.top);
  const factor = Math.exp(-event.deltaY * 0.001);
  state.viewport.scale = clamp(state.viewport.scale * factor, 0.35, 2.8);
  state.viewport.x = event.clientX - rect.left - before.x * state.viewport.scale;
  state.viewport.y = event.clientY - rect.top - before.y * state.viewport.scale;
}, { passive: false });

els.clusterList.addEventListener('click', event => {
  const row = event.target.closest('[data-cluster]');
  if (row) drillCluster(row.dataset.cluster);
});

els.inspector.addEventListener('click', event => {
  const row = event.target.closest('[data-node]');
  if (row) renderNode(row.dataset.node);
});

els.findingsList.addEventListener('click', event => {
  const row = event.target.closest('[data-node]');
  if (row) renderNode(row.dataset.node);
});

document.getElementById('overviewButton').addEventListener('click', overview);
document.getElementById('fitButton').addEventListener('click', () => {
  state.needsFit = true;
  state.viewport = { x: 0, y: 0, scale: 1 };
});
document.getElementById('llmButton').addEventListener('click', () => renderFindings('llm'));

document.querySelectorAll('[data-source]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-source]').forEach(item => item.classList.remove('is-active'));
    button.classList.add('is-active');
    renderFindings(button.dataset.source);
  });
});

els.search.addEventListener('input', () => {
  state.query = els.search.value;
  renderClusters();
  renderFindings();
});

window.addEventListener('resize', resize);

function fmt(value) {
  return new Intl.NumberFormat().format(value || 0);
}

function setOverviewModeLabel() {
  const shown = state.graph?.nodes?.length || 0;
  const total = state.graph?.total_clusters || shown;
  const hidden = state.graph?.hidden_clusters || 0;
  els.modeLabel.textContent = hidden ? `Cluster Map · ${shown} of ${total} shown` : 'Cluster Map';
}

function labelCandidates(nodes) {
  const ranked = [...nodes].sort((a, b) => labelScore(b) - labelScore(a));
  const limit = state.mode === 'clusters' ? Math.min(14, Math.ceil(nodes.length * 0.22)) : Math.min(22, Math.ceil(nodes.length * 0.18));
  return new Set(ranked.slice(0, limit).filter(labelScore).map(node => node.id));
}

function labelScore(node) {
  if (state.mode === 'clusters') {
    return (node.llm_finding_count || 0) * 100 + (node.finding_count || 0) * 6 + (node.risk_score || 0) * 18 + Math.sqrt(node.size || 1);
  }
  return (node.llm_finding_count || 0) * 100 + (node.finding_count || 0) * 12 + (node.risk_score || 0) * 20;
}

function screenToWorld(x, y) {
  return {
    x: (x - state.viewport.x) / state.viewport.scale,
    y: (y - state.viewport.y) / state.viewport.scale
  };
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function trim(value, length) {
  const text = String(value || '');
  return text.length > length ? `${text.slice(0, length - 1)}...` : text;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/`/g, '&#96;');
}

boot().catch(error => {
  els.inspector.innerHTML = `<div class="empty"><h2>Viewer failed to load</h2><p>${escapeHtml(error.message)}</p></div>`;
});
