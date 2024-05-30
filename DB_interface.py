from os import getenv
import mysql.connector
import pickle
import BlackScholesHeatmap
import BlackScholes


class DBOutput:
    def __init__(self, data):
        (self.row_id,
         self.date,
         self.volatility,
         self.underlying_price,
         self.exercise_price,
         self.time_to_expiration,
         self.annual_interest_rate,
         self.call_price,
         self.put_price,
         self.call_serialized,
         self.put_serialized) = data


def _db_connection():
    db = mysql.connector.connect(
        host='localhost',
        user=getenv('DB_USERNAME_OPTION_PRICER'),
        password=getenv('DB_PASSWORD_OPTION_PRICER'),
        database='Option_Pricer_DB'
    )

    # Table creation if needed
    db.cursor().execute('''
            CREATE TABLE IF NOT EXISTS option_pricer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATETIME,
                volatility FLOAT,
                underlying_price FLOAT,
                exercise_price FLOAT,
                time_to_expiration FLOAT,
                annual_interest_rate FLOAT,
                call_price FLOAT,
                put_price FLOAT,
                call_heatmap BLOB,
                put_heatmap BLOB
            );
        ''')
    return db, db.cursor()


def _db_disconnection(db, commit=False):
    if commit:
        db.commit()
    db.close()


def db_store_option_pricing(var, bsm_prices, heatmaps):
    db, cursor = _db_connection()

    # Data insertion
    db.start_transaction()
    cursor.execute('''
    INSERT INTO option_pricer (
        date,
        volatility, 
        underlying_price, 
        exercise_price, 
        time_to_expiration, 
        annual_interest_rate, 
        call_price,
        put_price,
        call_heatmap, 
        put_heatmap) 
    VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    ''', (var.volatility, var.underlying_price, var.exercise_price, var.time_to_expiration,
          var.annual_interest_rate, bsm_prices.call_price, bsm_prices.put_price, heatmaps.call_serialized,
          heatmaps.put_serialized))

    # Extract ID and date from the newly stored data
    new_row_id = cursor.lastrowid
    cursor.execute("SELECT date FROM option_pricer WHERE id = %s", (new_row_id,))
    new_row_date = cursor.fetchone()[0]
    _db_disconnection(db, commit=True)

    return new_row_id, new_row_date


def read_option_values(row_id):
    db, cursor = _db_connection()
    # Data reading
    cursor.execute('''
    SELECT id,
        date,
        volatility,
        underlying_price,
        exercise_price,
        time_to_expiration,
        annual_interest_rate,
        call_price,
        put_price,
        call_heatmap,
        put_heatmap
    FROM option_pricer WHERE id = %s ''', (row_id,))

    data = DBOutput(cursor.fetchone())

    _db_disconnection(db)

    return data


def find_next_id(current_id, next_or_prev):
    db, cursor = _db_connection()
    if next_or_prev == 'next':
        query = '''
                SELECT id
                FROM option_pricer
                WHERE id > %s
                ORDER BY id ASC
                LIMIT 1
            '''
    elif next_or_prev == 'prev':
        query = '''
                    SELECT id
                    FROM option_pricer
                    WHERE id < %s
                    ORDER BY id DESC
                    LIMIT 1
                '''
    cursor.execute(query, (current_id,))
    next_id_tuple = cursor.fetchone()

    if next_id_tuple is not None:
        next_id = next_id_tuple[0]
    else:
        next_id = 0

    _db_disconnection(db)
    return next_id


def max_id():
    db, cursor = _db_connection()
    #  check first if database is empty, for the first time it is created
    cursor.execute("SELECT COUNT(*) FROM option_pricer")
    if cursor.fetchone()[0] == 0:
        next_id = 0
    else:
        cursor.execute("SELECT MAX(id) FROM option_pricer")
        next_id_tuple = cursor.fetchone()
        next_id = next_id_tuple[0]

    _db_disconnection(db)

    return next_id


def db_data_repacking(db_data):
    call_df = pickle.loads(db_data.call_serialized)
    put_df = pickle.loads(db_data.put_serialized)
    heatmaps = BlackScholesHeatmap.HeatmapOutput(BlackScholesHeatmap.generate_heatmap(call_df),
                                                 BlackScholesHeatmap.generate_heatmap(put_df),
                                                 call_df,
                                                 put_df)
    bsm_prices = BlackScholes.BSPricerOutput(db_data.call_price, db_data.put_price)
    return heatmaps, bsm_prices


__all__ = ['DBOutput', 'db_store_option_pricing', 'read_option_values', 'find_next_id', 'max_id', 'db_data_repacking']
