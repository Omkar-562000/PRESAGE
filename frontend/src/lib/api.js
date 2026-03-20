function getApiOrigin() {
  if (typeof window === "undefined") {
    return "";
  }

  const { protocol, hostname, port, origin } = window.location;
  if (port === "5173") {
    return `${protocol}//${hostname}:5000`;
  }
  return origin;
}

export function getApiUrl(path) {
  return `${getApiOrigin()}${path}`;
}

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

export function getReport() {
  return fetchJson("/api/report");
}

export function getReportJsonUrl() {
  return getApiUrl("/api/report");
}

export function getReportPdfUrl() {
  return getApiUrl("/api/report/pdf");
}

export function triggerAttack(attackId) {
  return fetchJson(`/api/attack/${attackId}`, { method: "POST" });
}
