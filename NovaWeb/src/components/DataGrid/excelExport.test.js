import { buildXlsx, buildFileName, columnName, sanitizeSheetName, zipStore } from './excelExport';

const decode = (bytes) => Buffer.from(bytes).toString('utf8');

describe('columnName', () => {
  it('converte gli indici in lettere Excel', () => {
    expect(columnName(0)).toBe('A');
    expect(columnName(25)).toBe('Z');
    expect(columnName(26)).toBe('AA');
    expect(columnName(701)).toBe('ZZ');
    expect(columnName(702)).toBe('AAA');
  });
});

describe('sanitizeSheetName', () => {
  it('toglie i caratteri vietati e limita a 31 caratteri', () => {
    expect(sanitizeSheetName('Lotto/1: [test]?')).toBe('Lotto 1 test');
    expect(sanitizeSheetName('x'.repeat(50))).toHaveLength(31);
  });
  it('usa un valore di ripiego se il nome è vuoto', () => {
    expect(sanitizeSheetName('')).toBe('Dati');
    expect(sanitizeSheetName(null)).toBe('Dati');
    expect(sanitizeSheetName("''")).toBe('Dati');
  });
});

describe('buildFileName', () => {
  it('compone nome, selezione e data', () => {
    const name = buildFileName('Piano di Spedizione', 'Lotto: 1/2', new Date(2026, 8, 5));
    expect(name).toBe('Piano_di_Spedizione_Lotto_1_2_2026-09-05.xlsx');
  });
  it('funziona senza selezione', () => {
    expect(buildFileName('Piano', '', new Date(2026, 0, 31))).toBe('Piano_2026-01-31.xlsx');
  });
});

describe('zipStore', () => {
  it('produce uno zip con firma e directory finale', () => {
    const zip = zipStore([{ name: 'a.txt', data: Uint8Array.from([104, 105]) }]);
    expect(Array.from(zip.slice(0, 4))).toEqual([0x50, 0x4b, 0x03, 0x04]);
    expect(Array.from(zip.slice(-22, -18))).toEqual([0x50, 0x4b, 0x05, 0x06]);
  });
});

describe('buildXlsx', () => {
  const columns = ['Codice', 'Qta', 'Note'];
  const rows = [
    { Codice: '00123', Qta: 5, Note: 'a < b & "c"' },
    { Codice: 'B', Qta: null, Note: 'perché è così' },
  ];

  it('genera un pacchetto xlsx con tutte le parti richieste', () => {
    const text = decode(buildXlsx({ columns, rows, sheetName: 'Foglio' }));
    ['[Content_Types].xml', 'xl/workbook.xml', 'xl/styles.xml', 'xl/worksheets/sheet1.xml'].forEach((part) =>
      expect(text).toContain(part)
    );
    expect(text).toContain('name="Foglio"');
  });

  it('mantiene i numeri come numeri e i codici come testo, con escape XML', () => {
    const text = decode(buildXlsx({ columns, rows, sheetName: 'Foglio' }));
    expect(text).toContain('<c r="B2"><v>5</v></c>');
    expect(text).toContain('<t xml:space="preserve">00123</t>');
    expect(text).toContain('a &lt; b &amp; &quot;c&quot;');
    expect(text).toContain('perché è così'); // UTF-8 preservato
    expect(text).not.toContain('r="B3"'); // cella vuota omessa
  });

  it('imposta filtro automatico e riquadro bloccato sull\'intestazione', () => {
    const text = decode(buildXlsx({ columns, rows, sheetName: 'Foglio' }));
    expect(text).toContain('<autoFilter ref="A1:C3"/>');
    expect(text).toContain('state="frozen"');
  });

  it('non si rompe con zero righe', () => {
    const text = decode(buildXlsx({ columns, rows: [], sheetName: 'Foglio' }));
    expect(text).toContain('<autoFilter ref="A1:C1"/>');
  });
});
