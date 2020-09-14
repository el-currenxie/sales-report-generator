import caribou
import os


def update_db_struct(version, workspace, dbdir):
    print("migration")
    migrations_path = os.path.join(workspace, 'resource', 'sql', 'migrations')
    caribou.upgrade(
        db_url=dbdir, migration_dir=migrations_path, version=version)

    # # udpate record
    # reports_file_path = os.path.join(Path.home(),'Desktop','reports')
    # conn = sqlite3.connect(dbdir)
    # c = conn.cursor()
    # file_list = os.listdir(reports_file_path)
    # file_counter = 0

    # for filename in file_list:
    #     if filename.endswith(".csv"):
    #         c.execute("SELECT * FROM imported_files WHERE file_name=?", (filename,))
    #         if c.fetchone() is not None:
    #             df = pd.read_csv(os.path.join(reports_file_path,filename), sep='\t')

    #             try:
    #                 df.drop_duplicates('amazon-order-id', keep='first', inplace=True)
    #                 df.dropna(0, how='any', subset= ['item-price'], inplace = True)
    #                 df.dropna(0, how='any', subset=['currency'], inplace=True)
    #                 df.dropna(0, how='any', subset=['quantity-shipped'], inplace=True)
    #             except:
    #                 print("data operation error")
    #             try:
    #                 df = df[df['item-price'] != 0]
    #             except:
    #                 print("type error")

    #             for index, row in df.iterrows():
    #                 try:
    #                     c.execute("""
    #                     update sales
    #                     set
    #                         ship_address_1,
    #                         ship_address_2,
    #                         ship_address_3,
    #                         ship_city,
    #                         ship_state,
    #                         ship_postal_code,
    #                         ship_country,
    #                         buyer_name
    #                     where amazon_order_id
    #                     """,
    #                     (
    #                         row['ship-address-1'],
    #                         row['ship-address-2'],
    #                         row['ship-address-3'],
    #                         row['ship-city'],
    #                         row['ship-state'],
    #                         row['ship-postal-code'],
    #                         row['ship-country'],
    #                         row['buyer-name'],
    #                         row['amazon-order-id']
    #                     ))
    #                 except:
    #                     print(f"error importing transaction {row['amazon-order-id']}")
    # conn.commit()
    # conn.close()
    print("finish")
    return {
        "title": "Currenxie",
        "message": "DB Migrations DONE"
    }
