import akshare as ak
from sqlalchemy import create_engine, Column, Integer, String, text, select
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class StockIndex(Base):
    __tablename__ = 'stock_index'
    
    code = Column(String, primary_key=True)
    name = Column(String)
    publish_date = Column(String, nullable=True)

class IndexListings(Base):
    __tablename__ = 'index_listings'
    
    code = Column(String, primary_key=True)
    symbol = Column(String, primary_key=True)
    name = Column(String)
    publish_date = Column(String, nullable=True)

def write_index_listings_to_db(code: str, db_path='finance.db'):
    """
    Write index listings to SQLite database

    Parameters:
    -----------
    code : str
        The index code to fetch listings for
    db_path : str
        Path to SQLite database file
    """
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)

    try:
        index_records = []
        index_stock_cons_df = ak.index_stock_cons(code)
        for _, row in index_stock_cons_df.iterrows():
            index_records.append({
                'code': code,
                'symbol': row['品种代码'],
                'name': row['品种名称'],
                'publish_date': row['纳入日期']
            })

        # Write all records to database
        with engine.connect() as conn:
            # Clear existing data for this specific index only
            conn.execute(text("DELETE FROM index_listings WHERE code = :code"), {'code': code})
            conn.execute(text("INSERT INTO index_listings (code, symbol, name, publish_date) VALUES (:code, :symbol, :name, :publish_date)"),
                        index_records)
            conn.commit()
    except Exception as e:
        print(f"Error writing index listings to database: {str(e)}")
        raise

def write_stock_index_to_db(db_path='finance.db'):
    """
    Write stock index to SQLite database
    
    Parameters:
    -----------
    db_path : str
        Path to SQLite database file
    """
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)

    try:
        index_records = []
        index_stock_info_df = ak.index_stock_info()
        for _, row in index_stock_info_df.iterrows():
            index_records.append({
                'code': row['index_code'],
                'name': row['display_name'],
                'publish_date': row['publish_date']
            })
        
        # Write all records to database
        with engine.connect() as conn:
            # Clear existing data
            conn.execute(text("DELETE FROM stock_index"))
            conn.execute(text("INSERT INTO stock_index (code, name, publish_date) VALUES (:code, :name, :publish_date)"), 
                        index_records)
            conn.commit()
    except Exception as e:
        print(f"Error writing stock index to database: {str(e)}")
        raise

if __name__ == "__main__":
    print("Creating stock listings...")

    #write_stock_index_to_db()
    write_index_listings_to_db('000016')