#!/usr/bin/env python3
"""
Universal DB → Mermaid ER Diagram Generator
Поддерживает: SQLite, PostgreSQL, MySQL/MariaDB
Автор: сгенерировано Claude
"""

import os
import sys
import re


# ─────────────────────────────────────────────
#  Утилиты
# ─────────────────────────────────────────────

def sanitize(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def normalize_type(raw_type):
    t = (raw_type or "").upper()
    if any(x in t for x in ["INT", "SERIAL", "BIGINT", "SMALLINT"]):
        return "int"
    if any(x in t for x in ["CHAR", "TEXT", "CLOB", "VARCHAR", "ENUM", "UUID"]):
        return "string"
    if any(x in t for x in ["REAL", "FLOAT", "DOUBLE", "NUMERIC", "DECIMAL"]):
        return "float"
    if any(x in t for x in ["BOOL"]):
        return "bool"
    if any(x in t for x in ["DATE", "TIME", "TIMESTAMP"]):
        return "datetime"
    if "BLOB" in t or "BINARY" in t or "BYTEA" in t:
        return "blob"
    if "JSON" in t:
        return "json"
    return "string"


def build_mermaid(tables_data, relations):
    """
    tables_data: { table_name: [(col_name, col_type, is_pk), ...] }
    relations:   [(from_table, to_table, label), ...]
    """
    lines = ["# ER Диаграмма", "", "```mermaid", "erDiagram"]

    for table, columns in tables_data.items():
        lines.append(f"    {sanitize(table)} {{")
        for col_name, col_type, is_pk in columns:
            suffix = " PK" if is_pk else ""
            lines.append(f"        {col_type} {sanitize(col_name)}{suffix}")
        lines.append("    }")
        lines.append("")

    for from_t, to_t, label in relations:
        lines.append(f"    {sanitize(from_t)} ||--o{{ {sanitize(to_t)} : \"{label}\"")

    lines.append("```")
    return "\n".join(lines)


def save_and_report(mermaid, output_file="diagram.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(mermaid)
    print(f"\n✅ Диаграмма сохранена в '{output_file}'")
    print("   Открой файл в VS Code и нажми Ctrl+Shift+V\n")


# ─────────────────────────────────────────────
#  SQLite
# ─────────────────────────────────────────────

def from_sqlite(path):
    import sqlite3

    if not os.path.exists(path):
        print(f"❌ Файл не найден: {path}")
        sys.exit(1)

    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]

    tables_data = {}
    relations = []

    for table in tables:
        cur.execute(f"PRAGMA table_info('{table}')")
        cols = cur.fetchall()
        tables_data[table] = [
            (col[1], normalize_type(col[2]), bool(col[5]))
            for col in cols
        ]

        cur.execute(f"PRAGMA foreign_key_list('{table}')")
        for fk in cur.fetchall():
            ref_table = fk[2]
            relations.append((ref_table, table, "has"))

    conn.close()
    return tables_data, relations


# ─────────────────────────────────────────────
#  PostgreSQL
# ─────────────────────────────────────────────

def from_postgres(host, port, dbname, user, password, schema="public"):
    try:
        import psycopg2
    except ImportError:
        print("❌ Установи psycopg2:  pip install psycopg2-binary")
        sys.exit(1)

    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """, (schema,))
    tables = [r[0] for r in cur.fetchall()]

    tables_data = {}
    relations = []

    for table in tables:
        # Колонки
        cur.execute("""
            SELECT c.column_name, c.data_type,
                   CASE WHEN pk.column_name IS NOT NULL THEN TRUE ELSE FALSE END AS is_pk
            FROM information_schema.columns c
            LEFT JOIN (
                SELECT ku.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage ku
                    ON tc.constraint_name = ku.constraint_name
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_name = %s AND tc.table_schema = %s
            ) pk ON pk.column_name = c.column_name
            WHERE c.table_name = %s AND c.table_schema = %s
            ORDER BY c.ordinal_position
        """, (table, schema, table, schema))
        cols = cur.fetchall()
        tables_data[table] = [
            (col[0], normalize_type(col[1]), col[2])
            for col in cols
        ]

        # Foreign keys
        cur.execute("""
            SELECT ccu.table_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_name = %s AND tc.table_schema = %s
        """, (table, schema))
        for fk in cur.fetchall():
            relations.append((fk[0], table, "has"))

    conn.close()
    return tables_data, relations


# ─────────────────────────────────────────────
#  MySQL / MariaDB
# ─────────────────────────────────────────────

def from_mysql(host, port, dbname, user, password):
    try:
        import pymysql
    except ImportError:
        print("❌ Установи pymysql:  pip install pymysql")
        sys.exit(1)

    conn = pymysql.connect(host=host, port=int(port), db=dbname, user=user, password=password)
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """, (dbname,))
    tables = [r[0] for r in cur.fetchall()]

    tables_data = {}
    relations = []

    for table in tables:
        cur.execute("""
            SELECT column_name, data_type, column_key
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """, (dbname, table))
        cols = cur.fetchall()
        tables_data[table] = [
            (col[0], normalize_type(col[1]), col[2] == "PRI")
            for col in cols
        ]

        cur.execute("""
            SELECT referenced_table_name
            FROM information_schema.key_column_usage
            WHERE table_schema = %s AND table_name = %s
              AND referenced_table_name IS NOT NULL
        """, (dbname, table))
        for fk in cur.fetchall():
            relations.append((fk[0], table, "has"))

    conn.close()
    return tables_data, relations


# ─────────────────────────────────────────────
#  Интерактивное меню
# ─────────────────────────────────────────────

def ask(prompt, default=None):
    if default:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"{prompt}: ").strip()


def menu_sqlite():
    print("\n── SQLite ──────────────────────────────")
    # Ищем файлы автоматически
    found = [f for f in os.listdir(".") if f.endswith((".sqlite3", ".db", ".sqlite"))]
    if found:
        print("Найденные файлы в текущей папке:")
        for i, f in enumerate(found, 1):
            print(f"  {i}. {f}")
        choice = ask("Введи номер файла или полный путь")
        if choice.isdigit() and 1 <= int(choice) <= len(found):
            path = found[int(choice) - 1]
        else:
            path = choice
    else:
        path = ask("Путь к файлу БД (например db.sqlite3)")
    return from_sqlite(path)


def menu_postgres():
    print("\n── PostgreSQL ──────────────────────────")
    host     = ask("Хост",     "localhost")
    port     = ask("Порт",     "5432")
    dbname   = ask("Имя БД")
    user     = ask("Пользователь", "postgres")
    password = ask("Пароль")
    schema   = ask("Схема",   "public")
    return from_postgres(host, port, dbname, user, password, schema)


def menu_mysql():
    print("\n── MySQL / MariaDB ─────────────────────")
    host     = ask("Хост",     "localhost")
    port     = ask("Порт",     "3306")
    dbname   = ask("Имя БД")
    user     = ask("Пользователь", "root")
    password = ask("Пароль")
    return from_mysql(host, port, dbname, user, password)


def main():
    print("╔══════════════════════════════════════╗")
    print("║   DB → Mermaid ER Diagram Generator  ║")
    print("╚══════════════════════════════════════╝")
    print()
    print("Выбери тип базы данных:")
    print("  1. SQLite  (.sqlite3 / .db)")
    print("  2. PostgreSQL")
    print("  3. MySQL / MariaDB")
    print()

    choice = ask("Твой выбор (1/2/3)").strip()

    if choice == "1":
        tables_data, relations = menu_sqlite()
    elif choice == "2":
        tables_data, relations = menu_postgres()
    elif choice == "3":
        tables_data, relations = menu_mysql()
    else:
        print("❌ Неверный выбор")
        sys.exit(1)

    output = ask("\nИмя выходного файла", "diagram.md")
    if not output.endswith(".md"):
        output += ".md"

    mermaid = build_mermaid(tables_data, relations)
    save_and_report(mermaid, output)


if __name__ == "__main__":
    main()
