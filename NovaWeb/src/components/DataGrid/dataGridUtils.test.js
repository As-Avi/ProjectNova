import { filterItems, sortItems, nextSort, compareValues } from './dataGridUtils';

const rows = [
  { cliente: 'Rossi', peso: '10', citta: 'Milano' },
  { cliente: 'bianchi', peso: '9', citta: 'Roma' },
  { cliente: 'Verdi', peso: '100', citta: '' },
  { cliente: 'Neri', peso: '2,5', citta: 'Torino' },
];
const columns = ['cliente', 'peso', 'citta'];

describe('sortItems', () => {
  test('ordina i numeri come numeri, non come testo', () => {
    expect(sortItems(rows, 'peso', 'asc').map((r) => r.peso)).toEqual(['2,5', '9', '10', '100']);
    expect(sortItems(rows, 'peso', 'desc').map((r) => r.peso)).toEqual(['100', '10', '9', '2,5']);
  });

  test('il testo ignora maiuscole/minuscole', () => {
    expect(sortItems(rows, 'cliente', 'asc').map((r) => r.cliente)).toEqual([
      'bianchi', 'Neri', 'Rossi', 'Verdi',
    ]);
  });

  test('i valori vuoti restano in fondo in entrambe le direzioni', () => {
    expect(sortItems(rows, 'citta', 'asc').at(-1).cliente).toBe('Verdi');
    expect(sortItems(rows, 'citta', 'desc').at(-1).cliente).toBe('Verdi');
  });

  test('senza direzione restituisce l\'array originale e non lo muta', () => {
    expect(sortItems(rows, 'peso', null)).toBe(rows);
    sortItems(rows, 'peso', 'asc');
    expect(rows[0].cliente).toBe('Rossi');
  });
});

describe('filterItems', () => {
  test('filtro per colonna (contiene, case-insensitive)', () => {
    expect(filterItems(rows, columns, { cliente: 'ROS' }, '')).toHaveLength(1);
  });

  test('ricerca globale su tutte le colonne', () => {
    expect(filterItems(rows, columns, {}, 'torino')).toHaveLength(1);
  });

  test('filtri combinati in AND', () => {
    expect(filterItems(rows, columns, { cliente: 'i' }, 'roma').map((r) => r.cliente)).toEqual(['bianchi']);
  });

  test('senza filtri restituisce le righe originali', () => {
    expect(filterItems(rows, columns, {}, '  ')).toBe(rows);
  });
});

test('nextSort cicla asc -> desc -> nessuno', () => {
  let s = { key: null, direction: null };
  s = nextSort(s, 'a');
  expect(s).toEqual({ key: 'a', direction: 'asc' });
  s = nextSort(s, 'a');
  expect(s).toEqual({ key: 'a', direction: 'desc' });
  s = nextSort(s, 'a');
  expect(s).toEqual({ key: null, direction: null });
  expect(nextSort({ key: 'a', direction: 'desc' }, 'b')).toEqual({ key: 'b', direction: 'asc' });
});

test('compareValues gestisce numeri e testo', () => {
  expect(compareValues('9', '10')).toBeLessThan(0);
  expect(compareValues('a2', 'a10')).toBeLessThan(0);
});
