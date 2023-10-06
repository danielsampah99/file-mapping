# importing necessary python packages.
import pandas as pd

# Load the .csv file exported from wholesale2b.com
wholesale2b_dataframe = pd.read_csv(r"wholesale2b.csv")

# Column structure of new dataframe based on the exported file from obyshi.com.
column_structure = ['SKU', 'ProductName', 'Supplier', 'Brand', 'CategoryId',
                    'SubcategoryId', 'ChildcategoryId', 'Manufacturer', 'ProductType',
                    'DownloadLink', 'Price', 'Discount', 'Wholesale', 'MapPrice',
                    'HandlingFee', 'Unit', 'Stock', 'IfStockEmpty', 'Upc', 'Image',
                    'ShippingPrice', 'SalesTaxPct', 'IsTopDeals', 'IsTodaysDeals',
                    'IsBulkProduct', 'MinimumBulk', 'MaximumBulk', 'ReturnPolicy',
                    'AvgShippingDays', 'Attribute', 'IsDropshipping', 'Status', 'Type',
                    'Description']

# Define a dictionary to map old column names to new column names
column_mapping = {
    'sku': 'SKU',
    'title': 'ProductName',
    'supplier_name': 'Supplier',
    'brand': 'Brand',
    'w2b_category_1': 'CategoryId',
    'w2b_category_2': 'SubcategoryId',
    'w2b_category_3': 'ChildcategoryId',
    'na_manufacturer': 'Manufacturer',
    'na_producttype': 'ProductType',
    'large_image_url_250x250': 'DownloadLink',
    'retail_price': 'Price',
    'na_supplier_name': 'Discount',
    'wholesale': 'Wholesale',
    'map_price': 'MapPrice',
    'handling_fee': 'HandlingFee',
    'na_unit': 'Unit',
    'stock': 'Stock',
    'na_in_stock': 'IfStockEmpty',
    'upc': 'Upc',
    'original_image_url': 'Image',
    'shipping_price': 'ShippingPrice',
    'sales_tax_pct': 'SalesTaxPct',
    'na_istopdeals': 'IsTopDeals',
    'na_istodaysdeals': 'IsTodaysDeals',
    'na_isbulkproduct': 'IsBulkProduct,',
    'na_minimumbulk': 'MinimumBulk',
    'na_maximumbulk': 'MaximumBulk',
    'return_policy': 'ReturnPolicy',
    'avg_shipping_days': 'AvgShippingDays',
    'na_attribute': 'Attribute',
    'na_isdropshipping': 'IsDropshipping',
    'na_status': 'Status',
    'na_type': 'Type',
    'description_plain': 'Description',
}

# Create a new dataframe with a column structure of the obyshi.csv file.
new_dataframe = pd.DataFrame({column_name: [] for column_name in column_structure})

# Iterate through the rows in the wholesale2b dataframe.
for index, row in wholesale2b_dataframe.iterrows():
    new_row = {}

    # Iterate through the column mapping dictionary.
    for source_column, target_column in column_mapping.items():
        if not source_column.startswith("na_"):
            new_row[target_column] = row[source_column]

    # Append the new row to the new_dataframe.
    new_dataframe = new_dataframe._append(new_row, ignore_index=True)

# Columns to make 0 and 1.
columns_to_zero = ["Manufacturer", "ProductType", "IsTopDeals", "IsTodaysDeals", "IsBulkProduct", "MinimumBulk",
                   "MaximumBulk"]
columns_to_one = ["IsDropshipping", "Status", "Type"]

new_dataframe.loc[:, columns_to_zero] = 0
new_dataframe.loc[:, columns_to_one] = 1

# Save the new dataframe to a new .csv file.
new_dataframe.to_csv("upload to obyshi.com.csv", index=False, mode="w")
