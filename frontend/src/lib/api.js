export async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`${url} failed with ${response.status}`);
  }
  return response.json();
}

export function getState() {
  return fetchJson("/api/state");
}

export function triggerAttack(attackId) {
  return fetchJson(`/api/attack/${attackId}`, { method: "POST" });
}
