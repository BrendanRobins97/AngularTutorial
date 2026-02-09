let activeSessionId = null;

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

async function refreshSessions() {
  const sessions = await api('/api/sessions');
  const host = document.getElementById('sessions');
  host.innerHTML = '';
  for (const s of sessions) {
    const el = document.createElement('div');
    el.className = 'session';
    el.innerHTML = `
      <strong>${s.title}</strong>
      <div class="meta">Status: ${s.status}</div>
      <div class="meta">Audio: ${s.audio_path}</div>
      ${s.transcript ? `<pre>${s.transcript}</pre>` : `<button data-id="${s.id}">Transcribe</button>`}
    `;
    host.appendChild(el);
  }
  host.querySelectorAll('button[data-id]').forEach(btn => {
    btn.addEventListener('click', async () => {
      try {
        await api(`/api/sessions/${btn.dataset.id}/transcribe`, { method: 'POST' });
        await refreshSessions();
      } catch (e) {
        alert(e.message);
      }
    });
  });
}

document.getElementById('startBtn').addEventListener('click', async () => {
  const title = document.getElementById('title').value || 'Untitled Session';
  try {
    const result = await api('/api/sessions/start', { method: 'POST', body: JSON.stringify({ title }) });
    activeSessionId = result.session_id;
    document.getElementById('status').textContent = `Recording... session #${activeSessionId}`;
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
    await refreshSessions();
  } catch (e) {
    alert(e.message);
  }
});

document.getElementById('stopBtn').addEventListener('click', async () => {
  if (!activeSessionId) return;
  try {
    await api(`/api/sessions/${activeSessionId}/stop`, { method: 'POST' });
    document.getElementById('status').textContent = `Stopped session #${activeSessionId}`;
    activeSessionId = null;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    await refreshSessions();
  } catch (e) {
    alert(e.message);
  }
});

refreshSessions();
