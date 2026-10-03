/* Shared log reader for the Report and Paper pages.
   Logs stay in localStorage. Prefer the selected child's key
   (daily-log-entries__<childId>). If that key is missing, fall back
   to the unscoped key. Never mix another child's logs in. */
(function (root) {
  var PREFIX = "playbook:";

  function activeChildId() {
    try {
      var raw = localStorage.getItem(PREFIX + "active-child-id");
      if (raw == null) return "";
      var id = String(raw).trim();
      if (!id) return "";
      if (id.charAt(0) === '"' || id.charAt(0) === "{") {
        try {
          var parsed = JSON.parse(id);
          if (typeof parsed === "string") id = parsed;
        } catch (e) {}
      }
      return String(id || "").trim();
    } catch (e) {
      return "";
    }
  }

  function readRaw(key) {
    try { return localStorage.getItem(PREFIX + key); }
    catch (e) { return null; }
  }

  function parseList(raw) {
    if (raw == null) return null;
    try {
      var v = JSON.parse(raw);
      return Array.isArray(v) ? v : [];
    } catch (e) {
      return [];
    }
  }

  function withinDays(list, days) {
    if (days == null || days === "all") return list.slice();
    var n = Number(days);
    if (!isFinite(n) || n <= 0) return list.slice();
    var cut = new Date();
    cut.setDate(cut.getDate() - n);
    var iso = cut.toISOString().slice(0, 10);
    return list.filter(function (e) {
      return e && (!e.date || String(e.date) >= iso);
    });
  }

  function read(base, childId, days) {
    var id = (childId === undefined || childId === null || childId === "")
      ? activeChildId()
      : String(childId);
    var list = [];
    if (id) {
      var scopedRaw = readRaw(base + "__" + id);
      if (scopedRaw != null) list = parseList(scopedRaw) || [];
      else list = parseList(readRaw(base)) || [];
    } else {
      list = parseList(readRaw(base)) || [];
    }
    return withinDays(list, days);
  }

  root.PlaybookLogs = { read: read, activeChildId: activeChildId };
})(typeof window !== "undefined" ? window : this);
