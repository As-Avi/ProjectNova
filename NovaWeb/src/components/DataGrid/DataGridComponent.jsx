import { useCallback, useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import Form from 'react-bootstrap/Form';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSort, faSortUp, faSortDown, faXmark, faFileExcel } from '@fortawesome/free-solid-svg-icons';
import configData from '../../config.json';
import { filterItems, sortItems, nextSort } from './dataGridUtils';
import { buildXlsx, buildFileName, downloadXlsx } from './excelExport';
import './DataGridComponent.css';

const TITLE = 'Piano di Spedizione';
const LANGUAGE = 'Italian';

const authConfig = {
  auth: { username: configData.USER_NAME, password: configData.PASSWORD },
};

const sortIcon = (sort, column) => {
  if (sort.key !== column) return faSort;
  return sort.direction === 'asc' ? faSortUp : faSortDown;
};

const ariaSort = (sort, column) => {
  if (sort.key !== column) return 'none';
  return sort.direction === 'asc' ? 'ascending' : 'descending';
};

export default function DataGridComponent() {
  const configId = configData.MENU;

  const [comboItems, setComboItems] = useState([]);
  const [selected, setSelected] = useState(null); // null = nessuna selezione ancora fatta
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [sort, setSort] = useState({ key: null, direction: null });
  const [globalFilter, setGlobalFilter] = useState('');
  const [columnFilters, setColumnFilters] = useState({});

  // Elenco delle voci del combo, caricato una volta sola.
  useEffect(() => {
    const controller = new AbortController();
    axios
      .get(
        `${configData.SERVER_URL}combo?config=${encodeURIComponent(configId)}&language=${LANGUAGE}`,
        { ...authConfig, signal: controller.signal }
      )
      .then((res) => setComboItems(res.data.values ?? []))
      .catch((err) => {
        if (!axios.isCancel(err)) console.error('Error fetching combo:', err);
      });
    return () => controller.abort();
  }, [configId]);

  // Dati della griglia: si ricaricano al cambio di selezione; una richiesta obsoleta viene annullata.
  useEffect(() => {
    if (selected === null) return undefined;
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    axios
      .get(
        `${configData.SERVER_URL}view?config=${encodeURIComponent(configId)}&language=${LANGUAGE}&filter=${encodeURIComponent(selected)}`,
        { ...authConfig, signal: controller.signal }
      )
      .then((res) => {
        const data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
        setItems(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        if (axios.isCancel(err)) return;
        console.error('Error fetching data:', err);
        setItems([]);
        setError('Impossibile caricare i dati.');
        setLoading(false);
      });
    return () => controller.abort();
  }, [selected, configId]);

  // Le colonne derivano dalle chiavi della prima riga.
  const columns = useMemo(() => (items.length > 0 ? Object.keys(items[0]) : []), [items]);

  // Ordinamento e filtri restano finché le colonne non cambiano; altrimenti si azzerano.
  useEffect(() => {
    setSort({ key: null, direction: null });
    setColumnFilters({});
    setGlobalFilter('');
  }, [columns.join('|')]); // eslint-disable-line react-hooks/exhaustive-deps

  const visibleItems = useMemo(
    () => sortItems(filterItems(items, columns, columnFilters, globalFilter), sort.key, sort.direction),
    [items, columns, columnFilters, globalFilter, sort]
  );

  const hasActiveFilters =
    globalFilter.trim() !== '' || Object.values(columnFilters).some((v) => v && v.trim() !== '');

  const clearFilters = useCallback(() => {
    setGlobalFilter('');
    setColumnFilters({});
  }, []);

  // Esporta esattamente ciò che si vede: righe filtrate e ordinate, nello stesso ordine di colonne.
  const exportToExcel = useCallback(() => {
    try {
      const bytes = buildXlsx({ columns, rows: visibleItems, sheetName: selected });
      downloadXlsx(bytes, buildFileName(TITLE, selected));
    } catch (err) {
      console.error('Error exporting to Excel:', err);
      setError("Impossibile esportare i dati in Excel.");
    }
  }, [columns, visibleItems, selected]);

  const setColumnFilter = (column, value) =>
    setColumnFilters((prev) => ({ ...prev, [column]: value }));

  return (
    <div>
      <h4 className="bg-primary text-white text-center p-2">{TITLE}</h4>

      <div className="grid-toolbar">
        <Form.Group controlId="gridProcedure" className="grid-toolbar__select">
          <Form.Label>Seleziona:</Form.Label>
          <Form.Select value={selected ?? ''} onChange={(e) => setSelected(e.target.value)}>
            <option value=""></option>
            {comboItems.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        {columns.length > 0 && (
          <>
            <Form.Group controlId="gridSearch" className="grid-toolbar__search">
              <Form.Label>Cerca:</Form.Label>
              <Form.Control
                type="search"
                placeholder="Cerca in tutte le colonne"
                value={globalFilter}
                onChange={(e) => setGlobalFilter(e.target.value)}
              />
            </Form.Group>

            <div className="grid-toolbar__status" aria-live="polite">
              {visibleItems.length} di {items.length} righe
              {hasActiveFilters && (
                <button type="button" className="btn btn-link btn-sm" onClick={clearFilters}>
                  <FontAwesomeIcon icon={faXmark} /> Azzera filtri
                </button>
              )}
            </div>

            <button
              type="button"
              className="btn btn-success grid-toolbar__export"
              onClick={exportToExcel}
              disabled={loading || visibleItems.length === 0}
              title="Esporta in Excel le righe attualmente visibili (filtri e ordinamento inclusi)"
            >
              <FontAwesomeIcon icon={faFileExcel} /> Esporta in Excel
            </button>
          </>
        )}
      </div>

      {error && (
        <div className="alert alert-danger mx-2" role="alert">
          {error}
        </div>
      )}

      {loading && <div className="grid-message">Caricamento…</div>}

      {!loading && columns.length > 0 && (
        <div className="grid-scroll">
          <table className="table table-bordered table-hover nova-grid">
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column} aria-sort={ariaSort(sort, column)}>
                    <button
                      type="button"
                      className="nova-grid__sort"
                      onClick={() => setSort((current) => nextSort(current, column))}
                      title="Clicca per ordinare"
                    >
                      <span>{column}</span>
                      <FontAwesomeIcon
                        icon={sortIcon(sort, column)}
                        className={sort.key === column ? 'sort-icon sort-icon--active' : 'sort-icon'}
                      />
                    </button>
                  </th>
                ))}
              </tr>
              <tr className="nova-grid__filters">
                {columns.map((column) => (
                  <th key={column}>
                    <input
                      type="search"
                      className="form-control form-control-sm"
                      placeholder="Filtra…"
                      aria-label={`Filtra ${column}`}
                      value={columnFilters[column] ?? ''}
                      onChange={(e) => setColumnFilter(column, e.target.value)}
                    />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {visibleItems.map((item, rowIndex) => (
                <tr key={item.id ?? rowIndex}>
                  {columns.map((column) => (
                    <td key={column}>{item[column]}</td>
                  ))}
                </tr>
              ))}
              {visibleItems.length === 0 && (
                <tr className="nova-grid__empty">
                  <td colSpan={columns.length}>Nessuna riga corrisponde ai filtri.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
