#!/usr/bin/env python
"""Quick database verification script."""

import sqlite3

def check_db():
    from pathlib import Path
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    print('=== DISEASES TABLE CHECK ===')
    cursor.execute('SELECT COUNT(*) FROM diseases')
    count = cursor.fetchone()[0]
    print(f'Total diseases: {count}')

    cursor.execute('SELECT id, name_en FROM diseases LIMIT 5')
    print('Sample diseases:')
    for row in cursor.fetchall():
        print(f'  {row}')

    print('\n=== PREPARATIONS TABLE CHECK ===')
    cursor.execute('SELECT COUNT(*) FROM preparations')
    count = cursor.fetchone()[0]
    print(f'Total preparations: {count}')

    cursor.execute('SELECT id, name_en FROM preparations LIMIT 5')
    print('Sample preparations:')
    for row in cursor.fetchall():
        print(f'  {row}')

    print('\n=== SEARCH FOR SPECIFIC ITEMS ===')
    cursor.execute("SELECT id, name_en FROM diseases WHERE name_en LIKE '%cold%' OR name_en LIKE '%cough%' OR name_en LIKE '%rhinitis%' OR name_en LIKE '%running%nose%'")
    print('Diseases with cold/cough/rhinitis:')
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f'  {row}')
    else:
        print('  (none found)')

    cursor.execute("SELECT id, name_en FROM preparations WHERE name_en LIKE '%turmeric%' OR name_en LIKE '%triphala%' OR name_en LIKE '%neem%'")
    print('\nPreparations with turmeric/triphala/neem:')
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f'  {row}')
    else:
        print('  (none found)')

    print('\n=== ENTITY_I18N TABLE CHECK ===')
    cursor.execute('SELECT COUNT(*) FROM entity_i18n')
    count = cursor.fetchone()[0]
    print(f'Total i18n entries: {count}')

    conn.close()

if __name__ == '__main__':
    check_db()
