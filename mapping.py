# importing necessary python packages.
import pandas as pd
from fuzzywuzzy import process

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
column_mapping = {'sku': 'SKU',
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
                  'description_plain': 'Description', }

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

# Extracting wholesale2b category ids from the dataframe.
w2b_category_ids = new_dataframe['CategoryId']

# Obyshi category ids.
obyshi_category_ids = [
	'Health & Beauty', 'Health & Recovery', 'Vitamins & Supplements', 'Athletic & Fitness', 'Sports & Outside',
	'Appliances', 'Automotive', 'Electronics', 'Household Goods', 'Office Supplies & School', 'Pet Supplies',
	'Fashion', 'Digital Product', 'Arts & Crafts', 'Adults Only', 'Cell Phones & Accessories', 'Costumes & Props',
	'Fragrance & Perfume', 'General Merchandise', 'Grocery', 'Games & Hobbies', 'Home Improvement',
	'Home, Garden & Furniture', 'Jewelry', 'Kitchen', 'Musical Instruments', 'Watches'
]


# Loop through wholesale2b's list of category ids and find the most similar obyshi category id value.
def fuzzy_match(w2b_category_id):
	closest_match, score = process.extractOne(w2b_category_id, obyshi_category_ids)
	if score >= 50:
		return closest_match
	else:
		return w2b_category_id


new_dataframe["CategoryId"] = new_dataframe["CategoryId"].apply(fuzzy_match)

obyshi_category_mapping = {
	'Health & Beauty': 7, 'Health & Recovery': 8, 'Vitamins & Supplements': 12, 'Athletic & Fitness': 13,
	'Sports & Outside': 14, 'Appliances': 15, 'Automotive': 16, 'Electronics': 17, 'Household Goods': 18,
	'Office Supplies & School': 19, 'Pet Supplies': 20, 'Baby & Kids': 21, 'Fashion': 26, 'Digital Product': 27,
	'Arts & Crafts': 28, 'Adults Only': 29, 'Cell Phones & Accessories': 30, 'Costumes & Props': 31,
	'Fragrance & Perfume': 32, 'General Merchandise': 33, 'Grocery': 34, 'Games & Hobbies': 35, 'Home Improvement': 36,
	'Home, Garden & Furniture': 37, 'Jewelry': 38, 'Kitchen': 39, 'Musical Instruments': 40, 'Watches': 41,
	'Baby & Toddler': 14, 'Apparel & Clothing': 31, 'Computers & Networking': 27, 'Tools & Hardware': 36
}

# Replacing category names with id numbers.
new_dataframe['CategoryId'] = new_dataframe['CategoryId'].replace(obyshi_category_mapping)

# Writing the dataframe to a .csv file.
new_dataframe.to_csv("child category.csv", index=False)
