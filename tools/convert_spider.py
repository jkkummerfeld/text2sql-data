#!/usr/bin/env python3
"""
Many SQL queries may be semantically equivalent without being
identical. For our evaluation, we will treat as equivalent any pair of
queries <A, B> such that the tables in the FROM clause of A are the
same as the tables in the FROM clause of B (in any order) and the sub
clauses in the WHERE clause of A and B are the same (in any order,
provided parentheses are respected).
"""

from __future__ import print_function

import re
import string
import json
import sys
import argparse

LOGGING = False

###  Alterations:
###  
###  1. add_semicolon(query)
###  Adds a semicolon at the end of the SQL statement if it is missing.
###  
###  2. standardise_blank_spaces(query):
###  Ensures there is one blank space between each special character and word.
###  
###  3. capitalise(query, variables):
###  Converts all non-quoted sections of the query to uppercase.
###  
###  4. standardise_aliases(query):
###  Standardises the format of table aliases to be "table_name + count".
###  If a table does not have an alias, it adds an alias for the table.
###  
###  5. order_query(query):
###  Identifies the select, from and where clauses and orders the clause
###  components alphabetically using Python's sort() function.
###  
###  Limitations
###  - We do not handle quoted table names (a way to allow all sorts of crazy
###    names). We do not handle table names that are using keywords from mySQL
###  - We assume AND and OR are not mixed without brackets to indicate
###    precedence (it is legal SQL to do so, though a bad idea anyway).

SQL_RESERVED_WORDS = {w for w in """ACCOUNT ACTION ADD AFTER AGAINST AGGREGATE
ALGORITHM ALL ALTER ALWAYS ANALYSE ANALYZE AND ANY AS ASC ASCII ASENSITIVE AT
AUTOEXTEND_SIZE AUTO_INCREMENT AVG AVG_ROW_LENGTH BACKUP BEFORE BEGIN BETWEEN
BIGINT BINARY BINLOG BIT BLOB BLOCK BOOL BOOLEAN BOTH BTREE BY BYTE CACHE CALL
CASCADE CASCADED CASE CATALOG_NAME CESSIBLE CHAIN CHANGE CHANGED CHANNEL CHAR
CHARACTER CHARSET CHECK CHECKSUM CIPHER CLASS_ORIGIN CLIENT CLOSE COALESCE CODE
COLLATE COLLATION COLUMN COLUMNS COLUMN_FORMAT COLUMN_NAME COMMENT COMMIT
COMMITTED COMPACT COMPLETION COMPRESSED COMPRESSION CONCURRENT CONDITION
CONNECTION CONSISTENT CONSTRAINT CONSTRAINT_CATALOG CONSTRAINT_NAME
CONSTRAINT_SCHEMA CONTAINS CONTEXT CONTINUE CONVERT CPU CREATE CROSS CUBE
CURRENT CURRENT_DATE CURRENT_TIME CURRENT_TIMESTAMP CURRENT_USER CURSOR
CURSOR_NAME DATA DATABASE DATABASES DATAFILE DATE DATETIME DAY DAY_HOUR
DAY_MICROSECOND DAY_MINUTE DAY_SECOND DEALLOCATE DEC DECIMAL DECLARE DEFAULT
DEFAULT_AUTH DEFINER DELAYED DELAY_KEY_WRITE DELETE DESC DESCRIBE DES_KEY_FILE
DETERMINISTIC DIAGNOSTICS DIRECTORY DISABLE DISCARD DISK DISTINCT DISTINCTROW
DIV DO DOUBLE DROP DUAL DUMPFILE DUPLICATE DYNAMIC EACH ELSE ELSEIF ENABLE
ENCLOSED ENCRYPTION END ENDS ENGINE ENGINES ENUM ERROR ERRORS ESCAPE ESCAPED
EVENT EVENTS EVERY EXCHANGE EXECUTE EXISTS EXIT EXPANSION EXPIRE EXPLAIN EXPORT
EXTENDED EXTENT_SIZE FALSE FAST FAULTS FETCH FIELDS FILE FILE_BLOCK_SIZE FILTER
FIRST FIXED FLOAT FLOAT4 FLOAT8 FLUSH FOLLOWS FOR FORCE FOREIGN FORMAT FOUND
FROM FULL FULLTEXT FUNCTION GENERAL GENERATED GEOMETRY GEOMETRYCOLLECTION GET
GET_FORMAT GLOBAL GRANT GRANTS GROUP GROUP_REPLICATION HANDLER HASH HAVING HELP
HIGH_PRIORITY HOST HOSTS HOUR HOUR_MICROSECOND HOUR_MINUTE HOUR_SECOND
IDENTIFIED IF IGNORE IGNORE_SERVER_IDS IMPORT IN INDEX INDEXES INFILE
INITIAL_SIZE INNER INOUT INSENSITIVE INSERT INSERT_METHOD INSTALL INSTANCE INT
INT1 INT2 INT3 INT4 INT8 INTEGER INTERVAL INTO INVOKER IO IO_AFTER_GTIDS
IO_BEFORE_GTIDS IO_THREAD IPC IS ISOLATION ISSUER ITERATE JOIN JSON KEY KEYS
KEY_BLOCK_SIZE KILL LANGUAGE LAST LEADING LEAVE LEAVES LEFT LESS LEVEL LIKE
LIMIT LINEAR LINES LINESTRING LIST LOAD LOCAL LOCALTIME LOCALTIMESTAMP LOCK
LOCKS LOGFILE LOGS LONG LONGBLOB LONGTEXT LOOP LOW_PRIORITY MASTER
MASTER_AUTO_POSITION MASTER_BIND MASTER_CONNECT_RETRY MASTER_DELAY
MASTER_HEARTBEAT_PERIOD MASTER_HOST MASTER_LOG_FILE MASTER_LOG_POS
MASTER_PASSWORD MASTER_PORT MASTER_RETRY_COUNT MASTER_SERVER_ID MASTER_SSL
MASTER_SSL_CA MASTER_SSL_CAPATH MASTER_SSL_CERT MASTER_SSL_CIPHER
MASTER_SSL_CRL MASTER_SSL_CRLPATH MASTER_SSL_KEY MASTER_SSL_VERIFY_SERVER_CERT
MASTER_TLS_VERSION MASTER_USER MATCH MAXVALUE MAX_CONNECTIONS_PER_HOUR
MAX_QUERIES_PER_HOUR MAX_ROWS MAX_SIZE MAX_STATEMENT_TIME MAX_UPDATES_PER_HOUR
MAX_USER_CONNECTIONS MEDIUM MEDIUMBLOB MEDIUMINT MEDIUMTEXT MEMORY MERGE
MESSAGE_TEXT MICROSECOND MIDDLEINT MIGRATE MINUTE MINUTE_MICROSECOND
MINUTE_SECOND MIN_ROWS MOD MODE MODIFIES MODIFY MONTH MULTILINESTRING
MULTIPOINT MULTIPOLYGON MUTEX MYSQL_ERRNO NAME NAMES NATIONAL NATURAL NCHAR NDB
NDBCLUSTER NEVER NEW NEXT NO NODEGROUP NONBLOCKING NONE NOT NO_WAIT
NO_WRITE_TO_BINLOG NULL NUMBER NUMERIC NVARCHAR OFFSET OLD_PASSWORD ON ONE ONLY
OPEN OPTIMIZE OPTIMIZER_COSTS OPTION OPTIONALLY OPTIONS OR ORDER OUT OUTER
OUTFILE OWNER PACK_KEYS PAGE PARSER PARSE_GCOL_EXPR PARTIAL PARTITION
PARTITIONING PARTITIONS PASSWORD PHASE PLUGIN PLUGINS PLUGIN_DIR POINT POLYGON
PORT PRECEDES PRECISION PREPARE PRESERVE PREV PRIMARY PRIVILEGES PROCEDURE
PROCESSLIST PROFILE PROFILES PROXY PURGE QUARTER QUERY QUICK RANGE READ READS
READ_ONLY READ_WRITE REAL REBUILD RECOVER REDOFILE REDO_BUFFER_SIZE REDUNDANT
REFERENCES REGEXP RELAY RELAYLOG RELAY_LOG_FILE RELAY_LOG_POS RELAY_THREAD
RELEASE RELOAD REMOVE RENAME REORGANIZE REPAIR REPEAT REPEATABLE REPLACE
REPLICATE_DO_DB REPLICATE_DO_TABLE REPLICATE_IGNORE_DB REPLICATE_IGNORE_TABLE
REPLICATE_REWRITE_DB REPLICATE_WILD_DO_TABLE REPLICATE_WILD_IGNORE_TABLE
REPLICATION REQUIRE RESET RESIGNAL RESTORE RESTRICT RESUME RETURN
RETURNED_SQLSTATE RETURNS REVERSE REVOKE RIGHT RLIKE ROLLBACK ROLLUP ROTATE
ROUTINE ROW ROWS ROW_COUNT ROW_FORMAT RTREE SAVEPOINT SCHEDULE SCHEMA SCHEMAS
SCHEMA_NAME SECOND SECOND_MICROSECOND SECURITY SELECT SENSITIVE SEPARATOR
SERIAL SERIALIZABLE SERVER SESSION SET SHARE SHOW SHUTDOWN SIGNAL SIGNED SIMPLE
SLAVE SLOW SMALLINT SNAPSHOT SOCKET SOME SONAME SOUNDS SOURCE SPATIAL SPECIFIC
SQL SQLEXCEPTION SQLSTATE SQLWARNING SQL_AFTER_GTIDS SQL_AFTER_MTS_GAPS
SQL_BEFORE_GTIDS SQL_BIG_RESULT SQL_BUFFER_RESULT SQL_CACHE SQL_CALC_FOUND_ROWS
SQL_NO_CACHE SQL_SMALL_RESULT SQL_THREAD SQL_TSI_DAY SQL_TSI_HOUR
SQL_TSI_MINUTE SQL_TSI_MONTH SQL_TSI_QUARTER SQL_TSI_SECOND SQL_TSI_WEEK
SQL_TSI_YEAR SSL STACKED START STARTING STARTS STATS_AUTO_RECALC
STATS_PERSISTENT STATS_SAMPLE_PAGES STATUS STOP STORAGE STORED STRAIGHT_JOIN
STRING SUBCLASS_ORIGIN SUBJECT SUBPARTITION SUBPARTITIONS SUPER SUSPEND SWAPS
SWITCHES TABLE TABLES TABLESPACE TABLE_CHECKSUM TABLE_NAME TEMPORARY TEMPTABLE
TERMINATED TEXT THAN THEN TIME TIMESTAMP TIMESTAMPADD TIMESTAMPDIFF TINYBLOB
TINYINT TINYTEXT TO TRAILING TRANSACTION TRIGGER TRIGGERS TRUE TRUNCATE TYPE
TYPES UNCOMMITTED UNDEFINED UNDO UNDOFILE UNDO_BUFFER_SIZE UNICODE UNINSTALL
UNION UNIQUE UNKNOWN UNLOCK UNSIGNED UNTIL UPDATE UPGRADE USAGE USE USER
USER_RESOURCES USE_FRM USING UTC_DATE UTC_TIME UTC_TIMESTAMP VALIDATION VALUE
VALUES VARBINARY VARCHAR VARCHARACTER VARIABLES VARYING VIEW VIRTUAL WAIT
WARNINGS WEEK WEIGHT_STRING WHEN WHERE WHILE WITH WITHOUT WORK WRAPPER WRITE
X509 XA XID XML XOR YEAR YEAR_MONTH ZEROFILL EXCEPT INTERSECT""".split()}

def add_semicolon(query):
    query = query.strip()
    if len(query) > 0 and query[-1] != ';':
        return query + ';'
    return query

def update_quotes(char, in_single, in_double):
    if char == '"' and not in_single:
        in_double = not in_double
    elif char == "'" and not in_double:
        in_single = not in_single
    return in_single, in_double

def standardise_blank_spaces(query):
    # split on special characters except _.:-
    in_squote, in_dquote = False, False
    tmp_query = []
    pos = 0
    while pos < len(query):
        char = query[pos]
        pos += 1
        # Handle whether we are in quotes
        if char in ["'", '"']:
            if not (in_squote or in_dquote):
                tmp_query.append(" ")
            in_squote, in_dquote = update_quotes(char, in_squote, in_dquote)
            tmp_query.append(char)
            if not (in_squote or in_dquote):
                tmp_query.append(" ")
        elif in_squote or in_dquote:
            tmp_query.append(char)
        elif char in "!=<>,;()[]{}+*/\\#":
            tmp_query.append(" ")
            tmp_query.append(char)
            while pos < len(query) and query[pos] in "!=<>+*" and char in "!=<>+*":
                tmp_query.append(query[pos])
                pos += 1
            tmp_query.append(" ")
        else:
            tmp_query.append(char)
    new_query = ''.join(tmp_query)

    # Remove blank spaces just inside quotes:
    tmp_query = []
    in_squote, in_dquote = False, False
    prev = None
    prev2 = None
    for char in new_query:
        skip = False
        for quote, symbol in [(in_squote, "'"), (in_dquote, '"')]:
            if quote:
                if char in " \n"  and prev == symbol:
                    skip = True
                    break
                if char in " \n"  and prev == "%" and prev2 == symbol:
                    skip = True
                    break
                elif char == symbol and prev in " \n":
                    tmp_query.pop()
                elif char == symbol and prev == "%" and prev2 in " \n":
                    tmp_query.pop(len(tmp_query) - 2)
        if skip:
            continue

        in_squote, in_dquote = update_quotes(char, in_squote, in_dquote)
        tmp_query.append(char)
        prev2 = prev
        prev = char
    new_query = ''.join(tmp_query)

    # Replace single quotes with double quotes where possible
    tmp_query = []
    in_squote, in_dquote = False, False
    pos = 0
    while pos < len(new_query):
        char = new_query[pos]
        if (not in_dquote) and char == "'":
            to_add = [char]
            pos += 1
            saw_double = False
            while pos < len(new_query):
                tchar = new_query[pos]
                if tchar == '"':
                    saw_double = True
                to_add.append(tchar)
                if tchar == "'":
                    break
                pos += 1
            if not saw_double:
                to_add[0] = '"'
                to_add[-1] = '"'
            tmp_query.append(''.join(to_add))
        else:
            tmp_query.append(char)

        in_squote, in_dquote = update_quotes(char, in_squote, in_dquote)

        pos += 1
    new_query = ''.join(tmp_query)

    # remove repeated blank spaces
    new_query = ' '.join(new_query.split())

    # Remove spaces that would break SQL functions
    new_query = "COUNT(".join(new_query.split("count ("))
    new_query = "LOWER(".join(new_query.split("lower ("))
    new_query = "MAX(".join(new_query.split("max ("))
    new_query = "MIN(".join(new_query.split("min ("))
    new_query = "SUM(".join(new_query.split("sum ("))
    new_query = "AVG(".join(new_query.split("avg ("))
    new_query = "COUNT(".join(new_query.split("COUNT ("))
    new_query = "LOWER(".join(new_query.split("LOWER ("))
    new_query = "MAX(".join(new_query.split("MAX ("))
    new_query = "AVG(".join(new_query.split("AVG ("))
    new_query = "MIN(".join(new_query.split("MIN ("))
    new_query = "SUM(".join(new_query.split("SUM ("))
    new_query = "COUNT( *".join(new_query.split("COUNT(*"))
    new_query = "YEAR(CURDATE())".join(new_query.split("YEAR ( CURDATE ( ) )"))

    return new_query

def subquery_range(current, pos, tokens, in_quote=False):
    if current is not None and tokens[pos] == 'SELECT' and (not in_quote):
        return (pos, current[1])
    elif tokens[pos] == '(' and (not in_quote):
        start = pos
        end = pos + 1
        depth = 1
        in_squote, in_dquote = False, False
        while depth > 0:
            for char in tokens[end]:
                in_squote, in_dquote = update_quotes(char, in_squote, in_dquote)
            if not (in_squote or in_dquote):
                if '(' in tokens[end]:
                    depth += 1
                elif ')' in tokens[end]:
                    depth -= 1
            end += 1
        return (start, end)
    elif current is not None and pos == current[1]:
        start = pos
        end = pos + 1
        depth = 1
        in_squote, in_dquote = False, False
        while depth > 0 and start > 0:
            for char in tokens[start]:
                in_squote, in_dquote = update_quotes(char, in_squote, in_dquote)
            if not (in_squote or in_dquote):
                if '(' in tokens[start]:
                    depth -= 1
                elif ')' in tokens[start]:
                    depth += 1
            start -= 1
        if start != 0:
            start += 1

        while end < len(tokens) and tokens[end] != ')':
            end += 1
        if end != len(tokens):
            end += 1
        return (start, end)
    else:
        return current

ALIAS_PATTERN = re.compile("[A-Za-z0-9_]*")
def standardise_aliases(query, schema):
    count = {} # dictionary storing how many times each table has been used
    aliases = {} # dictionary mapping old aliases to standardised aliases
    field_aliases = {}
    tokens = query.split()

    # insert AS and replace old alias name with new alias name
    current_subquery = (0, -1)
    seen_from = {}
    seen_where = {}
    in_quote = False
    if LOGGING: print("Starting tokens:", tokens)
    for i, word in enumerate(tokens):
        for part in word.split('"'):
            in_quote = not in_quote
        in_quote = not in_quote
        current_subquery = subquery_range(current_subquery, i, tokens, in_quote)
        if word == "FROM":
            if LOGGING: print("Seen from", current_subquery[0], i)
            if seen_from.get(current_subquery[0], None) is None:
                seen_from[current_subquery[0]] = i
        elif current_subquery[0] not in seen_from:
            seen_from[current_subquery[0]] = None

        if word == "WHERE" or word == 'ORDER' or word == 'GROUP':
            seen_where[current_subquery[0]] = i
        elif current_subquery[0] not in seen_where:
            seen_where[current_subquery[0]] = None

        if word in schema[0] and not seen_where[current_subquery[0]] and seen_from[current_subquery[0]]:
            count[word] = count.get(word, -1) + 1
            if len(tokens) < i+2 or tokens[i+1] != 'AS':
                tokens.insert(i+1, 'AS')
            alias = word + "alias"+ str(count[word])

            # Check if there is an alias there now
            has_alias = False
            if len(tokens) > i+2:
                if tokens[i+2] not in SQL_RESERVED_WORDS:
                    if re.fullmatch(ALIAS_PATTERN, tokens[i+2]) is not None:
                        has_alias = True

            # Update this occurrence and our mapping
            if has_alias:
                aliases[current_subquery[0], tokens[i+2]] = alias
                tokens[i+2] = alias
            else:
                aliases[current_subquery[0], word] = alias
                tokens.insert(i+2, alias)
        elif i > 2 and tokens[i - 1] == 'AS':
            if tokens[i-2] not in schema[0]:
                if LOGGING: print("Considering", tokens[i-2:i+1], current_subquery, seen_from[current_subquery[0]])
                word = "DERIVED_TABLE"
                if seen_from[current_subquery[0]] is None:
                    word = "DERIVED_FIELD"
                count[word] = count.get(word, -1) + 1
                alias = word + "alias"+ str(count[word])
                if seen_from[current_subquery[0]] is None:
###                    print("New field alias", current_subquery[0], tokens[i], alias)
                    field_aliases[tokens[i]] = alias
                else:
###                    print("New alias", current_subquery[0], tokens[i], alias)
                    aliases[current_subquery[0], tokens[i]] = alias
                tokens[i] = alias
    if LOGGING: print("New tokens:", tokens)

    # replace old alias names for the columns with new alias names
    current_subquery = (0, -1)
    if LOGGING:
        for alias in aliases:
            print(alias, aliases[alias])
        for field_alias in field_aliases:
            print(field_alias, field_aliases[field_alias])
    in_quote = False
    for i, word in enumerate(tokens):
        for part in word.split('"'):
            in_quote = not in_quote
        in_quote = not in_quote
        current_subquery = subquery_range(current_subquery, i, tokens, in_quote)
        if (current_subquery[0], word) in aliases:
            if len(tokens) > i + 1 and tokens[i+1] != "AS":
                tokens[i] = aliases[current_subquery[0], word]
        if word in SQL_RESERVED_WORDS and word not in schema[1]:
            continue
        parts = word.split('.')
        if len(parts) == 2:
            if LOGGING: print(current_subquery, parts[0], word)
            if (current_subquery[0], parts[0]) in aliases:
                table = aliases[current_subquery[0], parts[0]]
                field = parts[1]
                if field in field_aliases and 'DERIVED' in table:
                    field = field_aliases[parts[1]]
                tokens[i] = table +"."+ field
            else:
                for alias in aliases:
                    other = subquery_range((0, -1), alias[0], tokens)
                    if LOGGING: print("   ", alias, alias[1], parts[0], other[0], current_subquery[0], other[1], i)
                    if alias[1] == parts[0] and other[0] < current_subquery[0] and (other[1] == -1 or other[1] > i):
                        tokens[i] = aliases[alias] +'.'+ parts[1]
        elif len(parts) == 1:
            # if no alias is specified, find the table name in the schema. We
            # assume that no field name is used ambiguously.
            options = []
            sf = seen_from.get(current_subquery[0], None)
            sw = seen_where.get(current_subquery[0], None)
            done = False
            if LOGGING: print(i, word, parts, sf, sw)
            if sf is None or i < sf or (sw is not None and i > sw):
                for table in schema[0]:
###                    print(table, schema[0][table])
                    if word in schema[0][table]:
###                        print("Found", i, word, table, current_subquery)
                        for pair in aliases:
                            alias = aliases[pair]
                            start = alias.split("alias")[0]
                            if pair[0] == current_subquery[0] and start == table:
                                tokens[i] = alias +'.' + word
                                done = True
                                break
                        if done:
                            break
            if (not done) and word in field_aliases:
                tokens[i] = field_aliases[word]

    return ' '.join(tokens)

def tokens_for_chunk(tokens, chunk):
    return tokens[chunk[0]:chunk[1]+1]
def get_matching_chunk(tokens, chunks, pos, target, default=None):
    saw_between = False
    while pos < len(chunks):
        chunk = chunks[pos]
        if tokens[chunk[0]].upper() == "BETWEEN":
            saw_between = True
        if chunk[0] == chunk[1] and tokens[chunk[0]] == target:
            if target != "AND" or (not saw_between):
                return pos
        if saw_between and tokens[chunk[0]].upper() == 'AND':
            saw_between = False
        pos += 1
    return default
def sort_chunk_list(start, end, chunks, tokens, separator=","):
    to_rearrange = []
    pos = start
    while pos < end:
        npos = get_matching_chunk(tokens, chunks, pos + 1, separator)
        if npos is None or npos > end:
            npos = end - 1
        left = chunks[pos][0]
        right = chunks[npos][1]
        to_rearrange.append((' '.join(tokens[left:right+1]), pos, npos))
        pos = npos + 1

    if len(to_rearrange) > 0:
        to_rearrange.sort()
        min_pos = min([chunks[v[1]][0] for v in to_rearrange])
        max_pos = max([chunks[v[2]][1] for v in to_rearrange])
        ctokens = tokens[min_pos:max_pos+1]
        cpos = min_pos
        for info in to_rearrange:
            saw_between = False
            for i in range(info[1], info[2]+1):
                for j in range(chunks[i][0], chunks[i][1]+1):
                    token = ctokens[j - min_pos]
                    advance = False
                    if (chunks[i][1] - chunks[i][0]) > 1:
                        advance = True
                    if token != separator or (saw_between and separator == 'AND'):
                        advance = True
                    if advance:
                        tokens[cpos] = ctokens[j-min_pos]
                        cpos += 1
                    if token == 'BETWEEN':
                        saw_between = True
                    if saw_between and token == 'AND':
                        saw_between = False
            if cpos <= max_pos:
                tokens[cpos] = separator
            cpos += 1

def order_sequence(tokens, start, end, variables):
    # Note - using https://ronsavage.github.io/SQL/sql-92.bnf.html to assist in
    # this construction.

    # First, recurse to subqueries
    cpos = start + 1
    chunks = [(start, start)]
    in_quote = False
    while cpos < end:
        for part in tokens[cpos].split('"'):
            in_quote = not in_quote
        in_quote = not in_quote
        sub = subquery_range(None, cpos, tokens, in_quote)
        if sub is None:
            chunks.append((cpos, cpos))
            cpos += 1
        else:
            chunks.append((cpos, sub[1] - 1))
            order_sequence(tokens, sub[0], sub[1] - 1, variables)
            cpos = sub[1]

    # Handle SELECT
    cur_chunk = 0
    while cur_chunk < len(chunks):
        next_select = get_matching_chunk(tokens, chunks, cur_chunk, "SELECT")
        if next_select is None: break
        
        next_distinct = get_matching_chunk(tokens, chunks, next_select, "DISTINCT")
        next_all = get_matching_chunk(tokens, chunks, next_select, "ALL")
        if next_distinct == next_select + 1 or next_all == next_select + 1:
            next_select += 1

        next_from = get_matching_chunk(tokens, chunks, next_select, "FROM", len(chunks))

        sort_chunk_list(next_select + 1, next_from, chunks, tokens)

        cur_chunk = next_from
    
    # Handle = and !=
    for symbol in ["=", "!="]:
        cur_chunk = 0
        while cur_chunk < len(chunks):
            next_equals = get_matching_chunk(tokens, chunks, cur_chunk, symbol)
            if next_equals is None:
                break
            left = tokens_for_chunk(tokens, chunks[next_equals - 1])
            right = tokens_for_chunk(tokens, chunks[next_equals + 1])
            left_text = ' '.join(left)
            right_text = ' '.join(right)

            swap = \
                left_text < right_text or \
                left_text in variables or \
                left_text[0] in string.digits or \
                left_text[0] in ['"', "'", "("] or \
                ' ' in left_text or \
                '.' not in left_text

            if right_text in variables or right_text[0] in string.digits or right_text[0] in ['"', "'", "("] or ' ' in right_text or '.' not in right_text:
                swap = False

            if swap:
                cpos = chunks[next_equals - 1][0]
                for token in right:
                    tokens[cpos] = token
                    cpos += 1
                tokens[cpos] = symbol
                cpos += 1
                for token in left:
                    tokens[cpos] = token
                    cpos += 1

            cur_chunk = next_equals + 2

    #  - Table names in 'from'
    cur_chunk = 0
    while cur_chunk < len(chunks):
        next_from = get_matching_chunk(tokens, chunks, cur_chunk, "FROM")
        if next_from is None: break

        next_item = min(
            get_matching_chunk(tokens, chunks, next_from, "WHERE", len(chunks)),
            get_matching_chunk(tokens, chunks, next_from, "JOIN", len(chunks)),
            get_matching_chunk(tokens, chunks, next_from, "GROUP", len(chunks)),
            get_matching_chunk(tokens, chunks, next_from, "HAVING", len(chunks)),
            get_matching_chunk(tokens, chunks, next_from, "LIMIT", len(chunks)),
            get_matching_chunk(tokens, chunks, next_from, "ORDER", len(chunks)),
            get_matching_chunk(tokens, chunks, next_from, ";", len(chunks))
        )
        sort_chunk_list(next_from + 1, next_item, chunks, tokens)
        cur_chunk = next_item

    #  - Comparisons in 'where'
    cur_chunk = 0
    while cur_chunk < len(chunks):
        next_where = get_matching_chunk(tokens, chunks, cur_chunk, "WHERE")
        if next_where is None:
            if tokens[chunks[0][0]] != "SELECT" and tokens[chunks[1][1]] != "SELECT":
                next_where = 0
            else:
                break

        next_item = min(
            get_matching_chunk(tokens, chunks, next_where, "GROUP", len(chunks)),
            get_matching_chunk(tokens, chunks, next_where, "HAVING", len(chunks)),
            get_matching_chunk(tokens, chunks, next_where, "LIMIT", len(chunks)),
            get_matching_chunk(tokens, chunks, next_where, "ORDER", len(chunks)),
            get_matching_chunk(tokens, chunks, next_where, ";", len(chunks))
        )
        has_and = False
        has_or = False
        saw_between = False
        for v in range(next_where + 1, next_item):
            chunk = chunks[v]
            if tokens[chunk[0]] == "BETWEEN":
                saw_between = True
            if chunk[0] == chunk[1] and tokens[chunk[0]] == "AND":
                if not saw_between:
                    has_and = True
                else:
                    saw_between = False
            if chunk[0] == chunk[1] and tokens[chunk[0]] == "OR":
                has_or = True

        if not (has_and and has_or):
            min_pos = min([chunks[v][0] for v in range(next_where + 1, next_item)])
            max_pos = max([chunks[v][1] for v in range(next_where + 1, next_item)])
            ctokens = tokens[min_pos:max_pos+1]
            sort_chunk_list(next_where + 1, next_item, chunks, tokens, "AND")
            sort_chunk_list(next_where + 1, next_item, chunks, tokens, "OR")
        cur_chunk = next_item

def order_query(query, variables):
    tokens = query.split()
    order_sequence(tokens, 0, len(tokens)-1, variables)
    return ' '.join(tokens)

def capitalise(query, variables):
    ntokens = []
    in_squote, in_dquote = False, False
    for token in query.split():
        if token in variables or token in ["credit0", "level0", "level1", "number0", "number1", "year0", "business_rating0"]:
            ntokens.append(token)
        else:
            modified = []
            for char in token:
                # Record the modified character
                if in_squote or in_dquote:
                    modified.append(char)
                else:
                    modified.append(char.upper())

                # Handle whether we are in quotes
                in_squote, in_dquote = update_quotes(char, in_squote, in_dquote)
            ntokens.append(''.join(modified))

    return ' '.join(ntokens)

def question_tokenise(question):
    tokens = []
    for token in question.split():
        if token[0] in '"' + "'":
            tokens.append(token[0])
            token = token[1:]

        later = []
        while len(token) > 0 and (token[-1] in "'.,?!" or token[-1] == '"'):
            later.append(token[-1])
            token = token[:-1]
        if len(token) > 0:
            tokens.append(token)
        for t in later[::-1]:
            tokens.append(t)
    return ' '.join(tokens)

def is_num(token):
    return all(c in '1234567890.' for c in token)

punctuation = ['.', ',', '(', ')']
def standarise_file(original, log, skip):
    schemas = {}
    schema_info = json.load(open("tables.json"))

    with open("spider-schemas.csv", 'w') as write_file:
        print("Database name, Table Name, Field Name, Is Primary Key, Is Foreign Key, Type", file=write_file)
        for db in schema_info:
            name = db['db_id']
            all_words = set()
            schema = {}
            for i, column in enumerate(db['column_names']):
                table = '_'.join(db['table_names'][column[0]].split()).upper()
                field = '_'.join(column[1].split()).upper()
                schema.setdefault(table, set()).add(field)
                all_words.add(table)
                all_words.add(field)
                ctype = db['column_types'][i]
                primary = i in db['primary_keys']
                foreign =  i in db['foreign_keys']
                if i > 0:
                    print("{}, {}, {}, {}, {}, {}".format(name, table, field, primary, foreign, ctype), file=write_file)
            schemas[name] = (schema, all_words)

    # Canonicalise
    for example in original:
        schema = schemas[example['sentences'][0]['database']]
        query = example['sql-original'][0]
        question = example['sentences'][0]['original']

        if log:
            print(question)
            print(query)

        question = question_tokenise(question)

        if 'add_semicolon' not in skip:
            query = add_semicolon(query)
        if 'standardise_blank_spaces' not in skip:
            query = standardise_blank_spaces(query)
    
        # Variables
        variables = []
        tokens = question.split()
        current = (None, None)
        nquery = []
        prev = None
        for token in query.split():
            used = False
            if current[0] is not None:
                if token.endswith(current[0]):
                    current[1].append(token[:-1])
                    var = ' '.join(current[1])
                    if var[0] == '%' and var[-1] == '%' and len(var) > 2:
                        var = var[1:-1]
                    nquery.append('"' + "var"+ str(len(variables)) + '"')
                    variables.append(var)
                    current = (None, None)
                    used = True
                else:
                    current[1].append(token)
                    used = True
            elif token.startswith('"') or token.startswith("'"):
                if token.endswith(token[0]):
                    if len(token) > 2:
                        var = token[1:-1]
                        if var.endswith("/%"):
                            var = var[:-2]
                            nquery.append('"' + "var"+ str(len(variables)) + '/%"')
                        else:
                            if var[0] == '%' and var[-1] == '%':
                                var = var[1:-1]
                            nquery.append('"' + "var"+ str(len(variables)) + '"')
                        variables.append(var)
                        used = True
                else:
                    current = (token[0], [token[1:]])
                    used = True
            else:
                if token in tokens and token.upper() not in schema[1] and token not in punctuation:
                    nquery.append("var"+ str(len(variables)))
                    variables.append(token)
                    used = True
                elif is_num(token) and (prev != "LIMIT" or token != "1"):
                    nquery.append("var"+ str(len(variables)))
                    variables.append(token)
                    used = True

            if not used:
                nquery.append(token)
            prev = token
        if log:
            print(' '.join(nquery))
        query = ' '.join(nquery)
        final_variables = example['variables']
        for i, var in enumerate(variables):
            name = "var"+ str(i)
            location = 'sql-only'
            if var in question:
                location = 'both'
                example['sentences'][0]['variables'][name] = var
                question = name.join(question.split(var))
            final_variables.append({
                'example': var,
                'location': location,
                'name': name,
                'type': "unknown",
            })
        variables = ['var'+ str(i) for i in range(len(variables))]
        if 'capitalise' not in skip:
            query = capitalise(query, variables)
        if 'standardise_aliases' not in skip:
            query = standardise_aliases(query, schema)
        if 'order_query' not in skip:
            query = order_query(query, variables)

        example['sql'] = [query]
        example['sentences'][0]['text'] = question

        if log:
            print(example['sql'][0])
            print(question)
            print()

    # Merge duplicates
    final = []
    seen = {}
    for example in original:
        query = example['sql'][0]
        if example['sql'][0] in seen:
            seen[query].append(example['sentences'][0])
        else:
            final.append(example)
            seen[query] = example['sentences']

    # Print to file
    with open("spider.json", 'w') as write_file:
        to_print = json.dumps(final, indent=4, sort_keys=True)
        for line in to_print.split("\n"):
            line = line.rstrip()
            print(line, file=write_file)

def add_data(filename, split, data, seen):
    for example in json.load(open(filename)):
        question = example['question']
        query = ' '.join(example['query'].split())
        db = example['db_id']
        info = {
            "query-split": "N/A",
            "sentences": [
                {
                    "question-split": split,
                    "original": question,
                    "database": db,
                    "variables": {}
                }
            ],
            "sql-original": [
                query
            ],
            "variables": [
            ]
        }
        ours.append(info)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modifies SQL to have a consistent tokenization. Expects a list of filenames as stdin.')
    parser.add_argument('--testadv', help='Run advising test cases and exit.', action='store_true')
    parser.add_argument('--testatis', help='Run ATIS test cases and exit.', action='store_true')
    parser.add_argument('--testscholar', help='Run scholar test cases and exit.', action='store_true')
    parser.add_argument('--testgeo', help='Run geo test cases and exit.', action='store_true')
    parser.add_argument('--testyelp', help='Run yelp test cases and exit.', action='store_true')
    parser.add_argument('--log', help='Print SQL before and after.', action='store_true')
    parser.add_argument('--skip', help='Functions that should not be applied (choices are [add_semicolon, standardise_blank_spaces, capitalise, standardise_aliases, order_query]).')
    args = parser.parse_args()



    skip = set()
    if args.skip is not None:
        skip = {v for v in args.skip.split(",")}

    if not (args.testadv or args.testgeo or args.testatis or args.testscholar or args.testyelp):
        ours = []
        seen = {}
        add_data("train_spider.json", "train", ours, seen)
        add_data("train_others.json", "train", ours, seen)
        add_data("dev.json", "dev", ours, seen)

        standarise_file(ours, args.log, skip)

        # TODO:
        # - Automatically extract variables by finding stuff that occurs in both query and question
    else:
        sample_queries = [
            ("select * from student where student.s_id < 5",
            "SELECT * FROM STUDENT AS STUDENTalias0 WHERE STUDENTalias0.S_ID < 5 ;"),

            ("""select last_name
            from student
            where student.s_id < 5
            and student.first_name = "Bob" """,
            """SELECT LAST_NAME FROM STUDENT AS STUDENTalias0 WHERE STUDENTalias0.FIRST_NAME = "Bob" AND STUDENTalias0.S_ID < 5 ;"""),

            ("""select last_name
            from student
            where student.s_id < 5
            and student.first_name = 'Bob'""",
            """SELECT LAST_NAME FROM STUDENT AS STUDENTalias0 WHERE STUDENTalias0.FIRST_NAME = "Bob" AND STUDENTalias0.S_ID < 5 ;"""),

            ("""select i.name
            from instructor i, offering_instructor oi, course_offering co, course c
            where i.instructor_id = oi.instructor_id
            and co.offering_id = oi.offering_id
            and c.course_id = co.course_id
            and c.department = 'EECS'
            and c.number = 280""",
            """SELECT INSTRUCTORalias0.NAME FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , INSTRUCTOR AS INSTRUCTORalias0 , OFFERING_INSTRUCTOR AS OFFERING_INSTRUCTORalias0 WHERE COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "EECS" AND COURSEalias0.NUMBER = 280 AND OFFERING_INSTRUCTORalias0.INSTRUCTOR_ID = INSTRUCTORalias0.INSTRUCTOR_ID AND OFFERING_INSTRUCTORalias0.OFFERING_ID = COURSE_OFFERINGalias0.OFFERING_ID ;"""),

            ("""select i.name
            from instructor i, offering_instructor oi, course_offering co, course c
            where c.number = 280
            and oi.offering_id = co.offering_id
            and i.instructor_id = oi.instructor_id
            and c.department = 'EECS'
            and co.course_id = c.course_id""",
            """SELECT INSTRUCTORalias0.NAME FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , INSTRUCTOR AS INSTRUCTORalias0 , OFFERING_INSTRUCTOR AS OFFERING_INSTRUCTORalias0 WHERE COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "EECS" AND COURSEalias0.NUMBER = 280 AND OFFERING_INSTRUCTORalias0.INSTRUCTOR_ID = INSTRUCTORalias0.INSTRUCTOR_ID AND OFFERING_INSTRUCTORalias0.OFFERING_ID = COURSE_OFFERINGalias0.OFFERING_ID ;"""),

            ("""select *
            from student s
            where (s.admit_term > 2000 AND s.lastname = "Smith")
            OR (s.firstname = "Bob" AND s.admit_term = 2000);""",
            """SELECT * FROM STUDENT AS STUDENTalias0 WHERE ( STUDENTalias0.ADMIT_TERM = 2000 AND STUDENTalias0.FIRSTNAME = "Bob" ) OR ( STUDENTalias0.ADMIT_TERM > 2000 AND STUDENTalias0.LASTNAME = "Smith" ) ;"""),

            ("""select *
            from student s
            where (s.firstname = "Bob" AND s.admit_term = 2000)
            OR s.lastname = "Smith"
            OR s.admit_term > 2000;""",
            """SELECT * FROM STUDENT AS STUDENTalias0 WHERE ( STUDENTalias0.ADMIT_TERM = 2000 AND STUDENTalias0.FIRSTNAME = "Bob" ) OR STUDENTalias0.ADMIT_TERM > 2000 OR STUDENTalias0.LASTNAME = "Smith" ;"""),

            ("""SELECT I.NAME, I.INSTRUCTOR_ID, COUNT(I.NAME) AS TIMES_TAUGHT
            FROM INSTRUCTOR I, OFFERING_INSTRUCTOR OI, COURSE_OFFERING CO, COURSE C
            WHERE C.DEPARTMENT = ' EECS '
            AND C.NUMBER = 280
            AND C.COURSE_ID = CO.COURSE_ID
            AND CO.OFFERING_ID = OI.OFFERING_ID
            AND OI.INSTRUCTOR_ID = I.INSTRUCTOR_ID
            GROUP BY I.NAME
            ORDER BY TIMES_TAUGHT
            DESC
            LIMIT 5""",
            """SELECT COUNT( INSTRUCTORalias0.NAME ) AS DERIVED_FIELDalias0 , INSTRUCTORalias0.INSTRUCTOR_ID , INSTRUCTORalias0.NAME FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , INSTRUCTOR AS INSTRUCTORalias0 , OFFERING_INSTRUCTOR AS OFFERING_INSTRUCTORalias0 WHERE COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "EECS" AND COURSEalias0.NUMBER = 280 AND OFFERING_INSTRUCTORalias0.INSTRUCTOR_ID = INSTRUCTORalias0.INSTRUCTOR_ID AND OFFERING_INSTRUCTORalias0.OFFERING_ID = COURSE_OFFERINGalias0.OFFERING_ID GROUP BY INSTRUCTORalias0.NAME ORDER BY DERIVED_FIELDalias0 DESC LIMIT 5 ;"""),

            ("""select DEPARTMENT, NUMBER, NAME
            from COURSE
            where lower(DESCRIPTION) like \"% artificial intelligence %\"
            and credits=4;""",
            """SELECT COURSEalias0.DEPARTMENT , COURSEalias0.NAME , COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 WHERE COURSEalias0.CREDITS = 4 AND LOWER( COURSEalias0.DESCRIPTION ) LIKE \"%artificial intelligence%\" ;"""),

            ("""SELECT C.NAME , C.ADVISORY_REQUIREMENT , C.ENFORCED_REQUIREMENT 
            FROM COURSE AS C
            WHERE C.NUMBER = 595
            AND C.DEPARTMENT = ' EECS ' ;""",
            """SELECT COURSEalias0.ADVISORY_REQUIREMENT , COURSEalias0.ENFORCED_REQUIREMENT , COURSEalias0.NAME FROM COURSE AS COURSEalias0 WHERE COURSEalias0.DEPARTMENT = "EECS" AND COURSEalias0.NUMBER = 595 ;"""),

            ("""select *
            from PROGRAM_COURSE
            where workload >= (SELECT MIN(workload) FROM PROGRAM_COURSE)""",
            """SELECT * FROM PROGRAM_COURSE AS PROGRAM_COURSEalias0 WHERE PROGRAM_COURSEalias0.WORKLOAD >= ( SELECT MIN( PROGRAM_COURSEalias1.WORKLOAD ) FROM PROGRAM_COURSE AS PROGRAM_COURSEalias1 ) ;"""),

            ("""SELECT C2.NUMBER
            FROM COURSE AS C2
            INNER JOIN PROGRAM_COURSE AS PC2 ON C2.COURSE_ID=PC2.COURSE_ID
            WHERE PC2.WORKLOAD=
               (SELECT MIN(PC.WORKLOAD)
                FROM PROGRAM_COURSE AS PC
                INNER JOIN COURSE AS C ON C.COURSE_ID=PC.COURSE_ID
                WHERE C.DEPARTMENT='EECS'
                AND (C.NUMBER=484 OR C.NUMBER=485))
                AND (C2.NUMBER=484 OR C2.NUMBER=485)""",
            """SELECT COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 INNER JOIN PROGRAM_COURSE AS PROGRAM_COURSEalias0 ON PROGRAM_COURSEalias0.COURSE_ID = COURSEalias0.COURSE_ID WHERE ( COURSEalias0.NUMBER = 484 OR COURSEalias0.NUMBER = 485 ) AND PROGRAM_COURSEalias0.WORKLOAD = ( SELECT MIN( PROGRAM_COURSEalias1.WORKLOAD ) FROM PROGRAM_COURSE AS PROGRAM_COURSEalias1 INNER JOIN COURSE AS COURSEalias1 ON PROGRAM_COURSEalias1.COURSE_ID = COURSEalias1.COURSE_ID WHERE ( COURSEalias1.NUMBER = 484 OR COURSEalias1.NUMBER = 485 ) AND COURSEalias1.DEPARTMENT = "EECS" ) ;"""),

            ("""select distinct C.NUMBER, C.NAME
            from COURSE C""",
            """SELECT DISTINCT COURSEalias0.NAME , COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 ;"""),

            ("""select *
            from student
            where student.s_id < 5;""",
            "SELECT * FROM STUDENT AS STUDENTalias0 WHERE STUDENTalias0.S_ID < 5 ;"),

            ("""select *
            from student
            where student.s_id < 5
            and student.first_name = 'Bob';""",
            """SELECT * FROM STUDENT AS STUDENTalias0 WHERE STUDENTalias0.FIRST_NAME = "Bob" AND STUDENTalias0.S_ID < 5 ;"""),

            ("""select i.name
            from instructor i, offering_instructor oi, course_offering co, course c
            where i.instructor_id = oi.instructor_id
            and oi.offering_id = co.offering_id
            and co.course_id = c.course_id
            and c.department = 'EECS'
            and c.number = 280;""",
            """SELECT INSTRUCTORalias0.NAME FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , INSTRUCTOR AS INSTRUCTORalias0 , OFFERING_INSTRUCTOR AS OFFERING_INSTRUCTORalias0 WHERE COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "EECS" AND COURSEalias0.NUMBER = 280 AND OFFERING_INSTRUCTORalias0.INSTRUCTOR_ID = INSTRUCTORalias0.INSTRUCTOR_ID AND OFFERING_INSTRUCTORalias0.OFFERING_ID = COURSE_OFFERINGalias0.OFFERING_ID ;"""),

            ("""select cr.department, cr.number from COURSE cl, COURSE_PREREQUISITE cp, COURSE cr where cl.course_id=cp.pre_course_id and cp.course_id=cr.course_id and cl.department = ' department0 ' and cl.number = number0;""",
            """SELECT COURSEalias1.DEPARTMENT , COURSEalias1.NUMBER FROM COURSE AS COURSEalias0 , COURSE AS COURSEalias1 , COURSE_PREREQUISITE AS COURSE_PREREQUISITEalias0 WHERE COURSEalias0.COURSE_ID = COURSE_PREREQUISITEalias0.PRE_COURSE_ID AND COURSEalias0.DEPARTMENT = "department0" AND COURSEalias0.NUMBER = number0 AND COURSEalias1.COURSE_ID = COURSE_PREREQUISITEalias0.COURSE_ID ;"""),

            ("""SELECT DISTINCT C.DEPARTMENT , C.NUMBER , C.NAME FROM COURSE AS C , PROGRAM_COURSE AS PC , COURSE_OFFERING AS CO , SEMESTER AS S WHERE C.COURSE_ID = CO.COURSE_ID AND C.COURSE_ID = PC.COURSE_ID AND PC.CATEGORY = ' ULCS ' AND CO.MONDAY = ' N ' AND CO.FRIDAY = ' N ' AND CO.SEMESTER = S.SEMESTER_ID AND S.SEMESTER = ' FA ' AND S.YEAR = 2016 ;""",
             """SELECT DISTINCT COURSEalias0.DEPARTMENT , COURSEalias0.NAME , COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , PROGRAM_COURSE AS PROGRAM_COURSEalias0 , SEMESTER AS SEMESTERalias0 WHERE COURSE_OFFERINGalias0.FRIDAY = "N" AND COURSE_OFFERINGalias0.MONDAY = "N" AND COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND PROGRAM_COURSEalias0.CATEGORY = "ULCS" AND PROGRAM_COURSEalias0.COURSE_ID = COURSEalias0.COURSE_ID AND SEMESTERalias0.SEMESTER = "FA" AND SEMESTERalias0.SEMESTER_ID = COURSE_OFFERINGalias0.SEMESTER AND SEMESTERalias0.YEAR = 2016 ;"""),

            ("""SELECT DISTINCT C.NUMBER , C.NAME FROM COURSE C , PROGRAM_COURSE PC , ( SELECT MAX ( WORKLOAD ) AS MAXWORK FROM PROGRAM_COURSE ) AS W WHERE C.COURSE_ID = PC.COURSE_ID AND PC.WORKLOAD = W.MAXWORK ;""",
             """SELECT DISTINCT COURSEalias0.NAME , COURSEalias0.NUMBER FROM ( SELECT MAX( PROGRAM_COURSEalias1.WORKLOAD ) AS DERIVED_FIELDalias0 FROM PROGRAM_COURSE AS PROGRAM_COURSEalias1 ) AS DERIVED_TABLEalias0 , COURSE AS COURSEalias0 , PROGRAM_COURSE AS PROGRAM_COURSEalias0 WHERE PROGRAM_COURSEalias0.COURSE_ID = COURSEalias0.COURSE_ID AND PROGRAM_COURSEalias0.WORKLOAD = DERIVED_TABLEalias0.DERIVED_FIELDalias0 ;"""),

            ("""select count(*) from COURSE c, COURSE_OFFERING co, SEMESTER s where c.course_id=co.course_id and s.year=2016 and s.semester='SU' and c.department=' department0 ' and c.number=number0;""",
            """SELECT COUNT( * ) FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , SEMESTER AS SEMESTERalias0 WHERE COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "department0" AND COURSEalias0.NUMBER = number0 AND SEMESTERalias0.SEMESTER = "SU" AND SEMESTERalias0.YEAR = 2016 ;"""),

            ("""SELECT COUNT ( * ) FROM COURSE_OFFERING CO , COURSE C WHERE C.COURSE_ID = CO.COURSE_ID AND C.DEPARTMENT = ' department0 ' AND C.NUMBER = number0 AND SEMESTER = 2070 AND START_TIME > ' 10:00:00 ' ;""",
             """SELECT COUNT( * ) FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 WHERE COURSE_OFFERINGalias0.SEMESTER = 2070 AND COURSE_OFFERINGalias0.START_TIME > "10:00:00" AND COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "department0" AND COURSEalias0.NUMBER = number0 ;"""),

            ("""SELECT COUNT ( DISTINCT CO.SEMESTER )
            FROM
            COURSE_OFFERING AS CO ,
            COURSE_OFFERING AS CO1 ,
            COURSE C ,
            COURSE C0 ,
            (
                SELECT COUNT ( * ) AS PREREQ_COUNT
                FROM COURSE C1 , COURSE C2 , COURSE_PREREQUISITE CP
                WHERE C1.DEPARTMENT = ' department0 ' AND
                C2.DEPARTMENT = ' department0 ' AND
                C1.NUMBER = number0 AND
                C2.NUMBER = number1 AND
                ( ( CP.PRE_COURSE_ID = C1.COURSE_ID AND
                    CP.COURSE_ID = C2.COURSE_ID ) OR
                  ( CP.PRE_COURSE_ID = C2.COURSE_ID AND
                    CP.COURSE_ID = C1.COURSE_ID ) )
            ) AS PC
            WHERE
            PC.PREREQ_COUNT = 0 AND
            C.DEPARTMENT = ' department0 ' AND
            C0.DEPARTMENT = ' department0 ' AND
            C.NUMBER = number0 AND
            C0.NUMBER = number1 AND
            CO.COURSE_ID = C.COURSE_ID AND
            CO1.COURSE_ID = C0.COURSE_ID AND
            CO.SEMESTER = CO1.SEMESTER ;""",
            """SELECT COUNT( DISTINCT COURSE_OFFERINGalias0.SEMESTER ) FROM ( SELECT COUNT( * ) AS DERIVED_FIELDalias0 FROM COURSE AS COURSEalias2 , COURSE AS COURSEalias3 , COURSE_PREREQUISITE AS COURSE_PREREQUISITEalias0 WHERE ( ( COURSEalias2.COURSE_ID = COURSE_PREREQUISITEalias0.COURSE_ID AND COURSEalias3.COURSE_ID = COURSE_PREREQUISITEalias0.PRE_COURSE_ID ) OR ( COURSEalias2.COURSE_ID = COURSE_PREREQUISITEalias0.PRE_COURSE_ID AND COURSEalias3.COURSE_ID = COURSE_PREREQUISITEalias0.COURSE_ID ) ) AND COURSEalias2.DEPARTMENT = "department0" AND COURSEalias2.NUMBER = number0 AND COURSEalias3.DEPARTMENT = "department0" AND COURSEalias3.NUMBER = number1 ) AS DERIVED_TABLEalias0 , COURSE AS COURSEalias0 , COURSE AS COURSEalias1 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias1 WHERE COURSE_OFFERINGalias1.SEMESTER = COURSE_OFFERINGalias0.SEMESTER AND COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "department0" AND COURSEalias0.NUMBER = number0 AND COURSEalias1.COURSE_ID = COURSE_OFFERINGalias1.COURSE_ID AND COURSEalias1.DEPARTMENT = "department0" AND COURSEalias1.NUMBER = number1 AND DERIVED_TABLEalias0.DERIVED_FIELDalias0 = 0 ;"""),

            ("""SELECT C.DEPARTMENT, C.NUMBER, C.NAME
            FROM
            COURSE C
            INNER JOIN COURSE_PREREQUISITE CP ON C.COURSE_ID = CP.PRE_COURSE_ID
            INNER JOIN COURSE C1 ON C1.COURSE_ID = CP.COURSE_ID
            WHERE
            C1.DEPARTMENT LIKE 'EECS' AND
            C1.NUMBER = 545;""",
            """SELECT COURSEalias0.DEPARTMENT , COURSEalias0.NAME , COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 INNER JOIN COURSE_PREREQUISITE AS COURSE_PREREQUISITEalias0 ON COURSEalias0.COURSE_ID = COURSE_PREREQUISITEalias0.PRE_COURSE_ID INNER JOIN COURSE AS COURSEalias1 ON COURSEalias1.COURSE_ID = COURSE_PREREQUISITEalias0.COURSE_ID WHERE COURSEalias1.DEPARTMENT LIKE "EECS" AND COURSEalias1.NUMBER = 545 ;"""),

            ("""SELECT TEMP.AREA
            FROM
            (
                SELECT A.AREA, COUNT(*) AS COUNT
                FROM AREA A
                INNER JOIN STUDENT_RECORD SR ON A.COURSE_ID = SR.COURSE_ID
                WHERE
                STUDENT_ID = 1 AND
                SR.GRADE LIKE "A"
                GROUP BY A.AREA
            ) AS TEMP
            WHERE
            TEMP.COUNT = 
            (
                SELECT COUNT(*) AS C
                FROM STUDENT_RECORD, AREA
                WHERE
                STUDENT_ID=1 AND
                GRADE LIKE "A" AND
                AREA.COURSE_ID = STUDENT_RECORD.COURSE_ID
                GROUP BY AREA.AREA
                ORDER BY C
                DESC
                LIMIT 1
            );""",
            """SELECT DERIVED_TABLEalias0.AREA FROM ( SELECT AREAalias0.AREA , COUNT( * ) AS DERIVED_FIELDalias0 FROM AREA AS AREAalias0 INNER JOIN STUDENT_RECORD AS STUDENT_RECORDalias0 ON STUDENT_RECORDalias0.COURSE_ID = AREAalias0.COURSE_ID WHERE STUDENT_RECORDalias0.GRADE LIKE "A" AND STUDENT_RECORDalias0.STUDENT_ID = 1 GROUP BY AREAalias0.AREA ) AS DERIVED_TABLEalias0 WHERE DERIVED_TABLEalias0.DERIVED_FIELDalias0 = ( SELECT COUNT( * ) AS DERIVED_FIELDalias1 FROM AREA AS AREAalias1 , STUDENT_RECORD AS STUDENT_RECORDalias1 WHERE STUDENT_RECORDalias1.COURSE_ID = AREAalias1.COURSE_ID AND STUDENT_RECORDalias1.GRADE LIKE "A" AND STUDENT_RECORDalias1.STUDENT_ID = 1 GROUP BY AREAalias1.AREA ORDER BY DERIVED_FIELDalias1 DESC LIMIT 1 ) ;"""),

            ("""select
                count(*) as number
                from
                COURSE_OFFERING co, COURSE c
                where
                c.course_id=co.course_id and
                co.semester=2070 and
                c.department=' department0 ' and
                c.number=number0 and
                start_time>='10:00:00' and
                end_time<='15:00:00';""",
            """SELECT COUNT( * ) AS DERIVED_FIELDalias0 FROM COURSE AS COURSEalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias0 WHERE COURSE_OFFERINGalias0.END_TIME <= "15:00:00" AND COURSE_OFFERINGalias0.SEMESTER = 2070 AND COURSE_OFFERINGalias0.START_TIME >= "10:00:00" AND COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = "department0" AND COURSEalias0.NUMBER = number0 ;"""),

            ("""SELECT *,
               COUNT (cp.pre_course_id) AS num_courses
               FROM course_prerequisite cp
               GROUP BY cp.pre_course_id
               ORDER BY num_courses DESC ;""",
            """SELECT * , COUNT( COURSE_PREREQUISITEalias0.PRE_COURSE_ID ) AS DERIVED_FIELDalias0 FROM COURSE_PREREQUISITE AS COURSE_PREREQUISITEalias0 GROUP BY COURSE_PREREQUISITEalias0.PRE_COURSE_ID ORDER BY DERIVED_FIELDalias0 DESC ;"""),

            ("""SELECT COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 INNER JOIN PROGRAM_COURSE AS PROGRAM_COURSEalias0 ON PROGRAM_COURSEalias0.COURSE_ID = COURSEalias0.COURSE_ID WHERE ( COURSEalias0.NUMBER = number0 OR COURSEalias0.NUMBER = number1 ) AND PROGRAM_COURSEalias0.WORKLOAD = ( SELECT MIN( PROGRAM_COURSEalias1.WORKLOAD ) FROM PROGRAM_COURSE AS PROGRAM_COURSEalias1 INNER JOIN COURSE AS COURSEalias1 ON PROGRAM_COURSEalias1.COURSE_ID = COURSEalias1.COURSE_ID WHERE ( COURSEalias1.NUMBER = number0 OR COURSEalias1.NUMBER = number1 ) AND COURSEalias1.DEPARTMENT = \"department0\" ) ;""",
             """SELECT COURSEalias0.NUMBER FROM COURSE AS COURSEalias0 INNER JOIN PROGRAM_COURSE AS PROGRAM_COURSEalias0 ON PROGRAM_COURSEalias0.COURSE_ID = COURSEalias0.COURSE_ID WHERE ( COURSEalias0.NUMBER = number0 OR COURSEalias0.NUMBER = number1 ) AND PROGRAM_COURSEalias0.WORKLOAD = ( SELECT MIN( PROGRAM_COURSEalias1.WORKLOAD ) FROM PROGRAM_COURSE AS PROGRAM_COURSEalias1 INNER JOIN COURSE AS COURSEalias1 ON PROGRAM_COURSEalias1.COURSE_ID = COURSEalias1.COURSE_ID WHERE ( COURSEalias1.NUMBER = number0 OR COURSEalias1.NUMBER = number1 ) AND COURSEalias1.DEPARTMENT = \"department0\" ) ;"""),

###            ("""SELECT COUNT( DISTINCT COURSE_OFFERINGalias0.SEMESTER ) FROM ( SELECT COUNT( * ) AS DERIVED_FIELDalias0 FROM COURSE AS COURSEalias2 , COURSE AS COURSEalias3 , COURSE_PREREQUISITE AS COURSE_PREREQUISITEalias0 WHERE ( ( COURSEalias2.COURSE_ID = COURSE_PREREQUISITEalias0.COURSE_ID AND COURSEalias3.COURSE_ID = COURSE_PREREQUISITEalias0.PRE_COURSE_ID ) OR ( COURSEalias2.COURSE_ID = COURSE_PREREQUISITEalias0.PRE_COURSE_ID AND COURSEalias3.COURSE_ID = COURSE_PREREQUISITEalias0.COURSE_ID ) ) AND COURSEalias2.DEPARTMENT = \"department0\" AND COURSEalias2.NUMBER = number0 AND COURSEalias3.DEPARTMENT = \"department0\" AND COURSEalias3.NUMBER = number1 ) AS DERIVED_TABLEalias0 , COURSE AS COURSEalias0 , COURSE AS COURSEalias1 , COURSE_OFFERING AS COURSE_OFFERINGalias0 , COURSE_OFFERING AS COURSE_OFFERINGalias1 WHERE COURSE_OFFERINGalias1.SEMESTER = COURSE_OFFERINGalias0.SEMESTER AND COURSEalias0.COURSE_ID = COURSE_OFFERINGalias0.COURSE_ID AND COURSEalias0.DEPARTMENT = \"department0\" AND COURSEalias0.NUMBER = number0 AND COURSEalias1.COURSE_ID = COURSE_OFFERINGalias1.COURSE_ID AND COURSEalias1.DEPARTMENT = \"department0\" AND COURSEalias1.NUMBER = number1 AND DERIVED_TABLEalias0.DERIVED_FIELDalias0 = 0 ;""",
###
        ]

        if args.testadv:
            if 'adv' not in args.fields:
                print("Are you sure you have the right fields file for Advising tests? Using:", args.fields)

        if args.testgeo:
            if 'geo' not in args.fields:
                print("Are you sure you have the right fields file for Geo tests? Using:", args.fields)
            sample_queries = [
                ("""SELECT STATE.STATE_NAME FROM STATE ;""",
                """SELECT STATEalias0.STATE_NAME FROM STATE AS STATEalias0 ;"""),

                ("""SELECT RIVER.RIVER_NAME FROM HIGHLOW , RIVER WHERE HIGHLOW.HIGHEST_ELEVATION = ( SELECT MAX( HIGHLOW.HIGHEST_ELEVATION ) FROM HIGHLOW ) AND RIVER.TRAVERSE = HIGHLOW.STATE_NAME ORDER BY RIVER.LENGTH DESC LIMIT 1 ;""",
                """SELECT RIVERalias0.RIVER_NAME FROM HIGHLOW AS HIGHLOWalias0 , RIVER AS RIVERalias0 WHERE HIGHLOWalias0.HIGHEST_ELEVATION = ( SELECT MAX( HIGHLOWalias1.HIGHEST_ELEVATION ) FROM HIGHLOW AS HIGHLOWalias1 ) AND RIVERalias0.TRAVERSE = HIGHLOWalias0.STATE_NAME ORDER BY RIVERalias0.LENGTH DESC LIMIT 1 ;"""),
            ]

        if args.testatis:
            if 'atis' not in args.fields:
                print("Are you sure you have the right fields file for ATIS tests? Using:", args.fields)
            sample_queries = [
                ("""SELECT DISTINCT flight_1.flight_id
                    FROM flight flight_1
                    WHERE flight_1.departure_time BETWEEN 0 AND 800 AND
                    flight_1.from_airport = DTW""",
                """SELECT DISTINCT FLIGHTalias0.FLIGHT_ID FROM FLIGHT AS FLIGHTalias0 WHERE FLIGHTalias0.DEPARTURE_TIME BETWEEN 0 AND 800 AND FLIGHTalias0.FROM_AIRPORT = DTW ;"""),
            ]

        if args.testscholar:
            if 'scholar' not in args.fields:
                print("Are you sure you have the right fields file for Scholar tests? Using:", args.fields)
            sample_queries = [
                ("""SELECT DISTINCT writes.paperId FROM writes, author,paper WHERE writes.authorId = author.authorID  AND writes.paperId = paper.paperId AND author.authorName = "Luke S Zettlemoyer" AND paper.year >= YEAR(CURDATE()) - 8""",
                 """SELECT DISTINCT WRITESalias0.PAPERID FROM AUTHOR AS AUTHORalias0 , PAPER AS PAPERalias0 , WRITES AS WRITESalias0 WHERE AUTHORalias0.AUTHORNAME = "Luke S Zettlemoyer" AND PAPERalias0.YEAR >= YEAR(CURDATE()) - 8 AND WRITESalias0.AUTHORID = AUTHORalias0.AUTHORID AND WRITESalias0.PAPERID = PAPERalias0.PAPERID ;"""),
                ("""SELECT DISTINCT writes.authorId FROM paper,writes,venue WHERE paper.venueId = venue.venueId AND paper.paperId = writes.paperId AND venue.venueName IN ("ICML","Science (New York, N.Y.)") GROUP BY writes.authorId having count(DISTINCT venue.venueId) = 2""",
                """SELECT DISTINCT WRITESalias0.AUTHORID FROM PAPER AS PAPERalias0 , VENUE AS VENUEalias0 , WRITES AS WRITESalias0 WHERE VENUEalias0.VENUEID = PAPERalias0.VENUEID AND VENUEalias0.VENUENAME IN ( "ICML" , "Science ( New York , N.Y. )" ) AND WRITESalias0.PAPERID = PAPERalias0.PAPERID GROUP BY WRITESalias0.AUTHORID HAVING COUNT( DISTINCT VENUEalias0.VENUEID ) = 2 ;"""),
                ("""SELECT DISTINCT paper.paperId FROM paper, paperKeyphrase, keyphrase WHERE paper.year = 2016 AND paper.paperId = paperKeyphrase.paperId AND paperKeyphrase.keyphraseId = keyphrase.keyphraseId AND keyphrase.keyphraseName IN ('Multiuser Receiver', 'Decision Feedback') GROUP BY paper.paperId HAVING count(DISTINCT keyphrase.keyphraseName)>1""",
                """SELECT DISTINCT PAPERalias0.PAPERID FROM KEYPHRASE AS KEYPHRASEalias0 , PAPER AS PAPERalias0 , PAPERKEYPHRASE AS PAPERKEYPHRASEalias0 WHERE KEYPHRASEalias0.KEYPHRASENAME IN ( "Multiuser Receiver" , "Decision Feedback" ) AND PAPERKEYPHRASEalias0.KEYPHRASEID = KEYPHRASEalias0.KEYPHRASEID AND PAPERalias0.PAPERID = PAPERKEYPHRASEalias0.PAPERID AND PAPERalias0.YEAR = 2016 GROUP BY PAPERalias0.PAPERID HAVING COUNT( DISTINCT KEYPHRASEalias0.KEYPHRASENAME ) > 1 ;"""),
            ]

        if args.testyelp:
            if 'yelp' not in args.fields:
                print("Are you sure you have the right fields file for Yelp tests? Using:", args.fields)
            sample_queries = [
                ("""select business_0.review_count from business as business_0 where business_0.name = \" business_name0 \" """,
                """SELECT BUSINESSalias0.REVIEW_COUNT FROM BUSINESS AS BUSINESSalias0 WHERE BUSINESSalias0.NAME = "business_name0" ;"""),
                ("""select count(distinct(review_0.text)) from business as business_0, review as review_0 where business_0.name = \" business_name0 \" and business_0.business_id = review_0.business_id ;""",
                """SELECT COUNT( DISTINCT ( REVIEWalias0.TEXT ) ) FROM BUSINESS AS BUSINESSalias0 , REVIEW AS REVIEWalias0 WHERE BUSINESSalias0.NAME = "business_name0" AND REVIEWalias0.BUSINESS_ID = BUSINESSalias0.BUSINESS_ID ;"""),
            ]

        schema = read_schema(args.fields)
        variables = {"number0", "department0"}
        for query, correct in sample_queries:
            # Canonicalise and print the output
            canonical = make_canonical(query, schema, variables)
            if canonical != correct:
                # Print the query, adjusting to avoid indentation
                print('\n'.join([part.strip() for part in query.split("\n")]))
                print(canonical)
                print(correct)
                LOGGING = True
                make_canonical(query, schema, variables)
                LOGGING = False
                print()

