// Funzioni pure per ordinamento e filtri della griglia (testabili senza React).

const collator = new Intl.Collator('it', { numeric: true, sensitivity: 'base' });

export function isEmpty(value) {
  return value === null || value === undefined || value === '';
}

// Converte in numero solo se il valore è davvero numerico (accetta anche la virgola decimale).
function toNumber(value) {
  if (typeof value === 'number') return value;
  if (typeof value !== 'string') return NaN;
  const trimmed = value.trim();
  if (trimmed === '' || !/^[-+]?\d+([.,]\d+)?$/.test(trimmed)) return NaN;
  return Number(trimmed.replace(',', '.'));
}

// Confronto tra due valori: numerico se entrambi numeri, altrimenti testuale "naturale".
// I valori vuoti finiscono sempre in fondo (gestito da sortItems).
export function compareValues(a, b) {
  const na = toNumber(a);
  const nb = toNumber(b);
  if (!Number.isNaN(na) && !Number.isNaN(nb)) return na - nb;
  return collator.compare(String(a), String(b));
}

// Restituisce le righe che soddisfano la ricerca globale e i filtri per colonna.
export function filterItems(items, columns, columnFilters, globalFilter) {
  const global = (globalFilter || '').trim().toLowerCase();
  const active = Object.entries(columnFilters || {})
    .map(([key, value]) => [key, (value || '').trim().toLowerCase()])
    .filter(([, value]) => value !== '');

  if (!global && active.length === 0) return items;

  return items.filter((item) => {
    const cellText = (key) => (isEmpty(item[key]) ? '' : String(item[key]).toLowerCase());
    if (!active.every(([key, value]) => cellText(key).includes(value))) return false;
    if (global && !columns.some((key) => cellText(key).includes(global))) return false;
    return true;
  });
}

// Ordina senza mutare l'array originale. direction: 'asc' | 'desc' | null.
export function sortItems(items, key, direction) {
  if (!key || !direction) return items;
  const factor = direction === 'desc' ? -1 : 1;
  return [...items].sort((x, y) => {
    const xe = isEmpty(x[key]);
    const ye = isEmpty(y[key]);
    if (xe || ye) return xe === ye ? 0 : xe ? 1 : -1; // vuoti sempre in fondo
    return compareValues(x[key], y[key]) * factor;
  });
}

// Ciclo del click sull'intestazione: nessun ordine -> asc -> desc -> nessun ordine.
export function nextSort(current, key) {
  if (current.key !== key) return { key, direction: 'asc' };
  if (current.direction === 'asc') return { key, direction: 'desc' };
  return { key: null, direction: null };
}
