
def upgrade(connection):
    sqls = [
        "ALTER TABLE sales add COLUMN buyer_name text ;",
        "ALTER TABLE sales add COLUMN ship_address_1 text ;",
        "ALTER TABLE sales add COLUMN ship_address_2 text ;",
        "ALTER TABLE sales add COLUMN ship_address_3 text ;",
        "ALTER TABLE sales add COLUMN ship_city text ;",
        "ALTER TABLE sales add COLUMN ship_state text ;",
        "ALTER TABLE sales add COLUMN ship_postal_code text ;",
        "ALTER TABLE sales add COLUMN ship_country text ;"
    ]
    connection.execute(sqls[0])
    connection.execute(sqls[1])
    connection.execute(sqls[2])
    connection.execute(sqls[3])
    connection.execute(sqls[4])
    connection.execute(sqls[5])
    connection.execute(sqls[6])
    connection.execute(sqls[7])



def downgrade(connection):
    pass