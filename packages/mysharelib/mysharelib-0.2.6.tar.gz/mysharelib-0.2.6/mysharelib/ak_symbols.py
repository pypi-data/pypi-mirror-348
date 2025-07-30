import akshare as ak
from sqlalchemy import create_engine, Column, Integer, String, text, select
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class StockListing(Base):
    __tablename__ = 'stock_listings'
    
    id = Column(Integer, primary_key=True)
    market = Column(String)  # 'SH', 'SZ', or 'HK'
    code = Column(String)
    name = Column(String)
    listing_date = Column(String, nullable=True)
    
def write_stock_lists_to_db(sh_list, sz_list, hk_list, db_path='finance.db'):
    """
    Write Shanghai, Shenzhen, and Hong Kong stock listings to SQLite database
    
    Parameters:
    -----------
    sh_list : DataFrame
        Shanghai stock listings
    sz_list : DataFrame
        Shenzhen stock listings 
    hk_list : DataFrame
        Hong Kong stock listings
    db_path : str
        Path to SQLite database file
    """
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    
    # Process Shanghai listings
    sh_records = []
    for _, row in sh_list.iterrows():
        sh_records.append({
            'market': 'SH',
            'code': row['证券代码'],
            'name': row['证券简称'],
            'listing_date': row['上市日期']
        })
    
    # Process Shenzhen listings    
    sz_records = []
    for _, row in sz_list.iterrows():
        sz_records.append({
            'market': 'SZ', 
            'code': row['A股代码'],
            'name': row['A股简称'],
            'listing_date': row['A股上市日期']
        })
        
    # Process Hong Kong listings
    hk_records = []
    for _, row in hk_list.iterrows():
        hk_records.append({
            'market': 'HK',
            'code': str(row['代码']),
            'name': row['名称'],
            'listing_date': None
        })
    
    # Write all records to database
    with engine.connect() as conn:
        # Clear existing data
        conn.execute(text("DELETE FROM stock_listings"))
        conn.execute(text("INSERT INTO stock_listings (market, code, name, listing_date) VALUES (:market, :code, :name, :listing_date)"), 
                    sh_records + sz_records + hk_records)
        conn.commit()

def create_stock_listing():
    """
    Create a new stock listing in SQLite database.
    """

    sh_list = ak.stock_info_sh_name_code()
    sz_list = ak.stock_info_sz_name_code()
    hk_list = ak.stock_hk_main_board_spot_em()

    print("Creating stock listings...")
    write_stock_lists_to_db(sh_list, sz_list, hk_list)

    # Verify the data
    engine = create_engine('sqlite:///finance.db')
    with engine.connect() as conn:
        result = conn.execute(text("SELECT market, COUNT(*) as count FROM stock_listings GROUP BY market"))
        for row in result:
            print(f"{row.market}: {row.count} listings")

if __name__ == "__main__":
    create_stock_listing()