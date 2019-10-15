
def upgrade(connection):
    sql = """
        ALTER TABLE sales 
        ADD 
        buyer_name text, 
        ship_address_1 text,
        ship_address_2 text,
        ship_address_3 text,
        ship_city text,
        ship_state text,
        ship_postal_code text,
        ship_country text;
    """
    connection.execute(sql)



def downgrade(connection):
    pass