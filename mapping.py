# importing necessary python packages.
import re
import pandas as pd
import os

# Load the .csv file exported from wholesale2b.com
wholesale2b_dataframe = pd.read_csv(r"/home/daniel/Downloads/Documents/wholesale2b_9k.csv")

print(set(wholesale2b_dataframe['w2b_category_1']))

# Columns of the new dataframe as seen in obyshi.com's exported file.
column_structure = ['SKU', 'ProductName', 'Supplier', 'Brand', 'CategoryId',
                    'SubcategoryId', 'ChildcategoryId', 'Manufacturer', 'ProductType',
                    'DownloadLink', 'Price', 'Discount', 'Wholesale', 'MapPrice',
                    'HandlingFee', 'Unit', 'Stock', 'IfStockEmpty', 'Upc', 'Image',
                    'ShippingPrice', 'SalesTaxPct', 'IsTopDeals', 'IsTodaysDeals',
                    'IsBulkProduct', 'MinimumBulk', 'MaximumBulk', 'ReturnPolicy',
                    'AvgShippingDays', 'Attribute', 'IsDropshipping', 'Status', 'Type',
					'Description', 'extra_img_1', 'extra_img_2', 'extra_img_3', 'extra_img_4', 
					'extra_img_5', 'extra_img_6', 'extra_img_7', 'extra_img_8', 'extra_img_9', 
					'extra_img_10'         ]

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
                  'attribute_list': 'Attribute',
                  'na_isdropshipping': 'IsDropshipping',
                  'na_status': 'Status',
                  'na_type': 'Type',
                  'description': 'Description', 
                  'extra_img_1': 'extra_img_1', 
                  'extra_img_2': 'extra_img_2', 
                  'extra_img_3': 'extra_img_3', 
                  'extra_img_4': 'extra_img_4', 
                  'extra_img_5': 'extra_img_5', 
                  'extra_img_6': 'extra_img_6', 
                  'extra_img_7': 'extra_img_7', 
                  'extra_img_8': 'extra_img_8', 
                  'extra_img_9': 'extra_img_9', 
                  'extra_img_10': 'extra_img_10'
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

# Extracting wholesale2b category ids from the dataframe.
w2b_category_ids = new_dataframe['CategoryId']

# Obyshi category ids.
obyshi_category_ids = [
	'Health & Beauty', 'Health & Recovery', 'Vitamins & Supplements', 'Sporting & Exercise',
	'Automotive Parts and Accessories', 'Electronics', 'Office & School Supplies', 'Pet Supplies',
	'Baby & Kids', 'Fashion', 'Arts, Crafts & DIYs', 'Adults Only', 'Cell Phones & Accessories', 'Costumes & Props',
	'Fragrance & Perfume', 'General Merchandise', 'Groceries & Whole Foods', 'Toys, Games & Hobbies',
	'Home Improvement', 'Home, Garden & Furniture', 'Jewelry', 'Kitchen & Appliances', 'Musical Instruments', 'Watches',
	'Mystic & Charming', 'Computers & Networking', 'Eyewear & Optics', 'Festive Occasions',
	'Marine & Boating', 'Knives & Multi-Tools', 'Bags, Luggage & Travel Gear', 'Boots & Shoes',
	'Vintage Telecommunication', 'Outdoors', 'Gifts & Gadgets', 'For Sports Fans', 'Safety & Security',
	'Tools & Hardware'
]

wholesale2b_to_obyshi_dictionary = {
	'Health & Beauty': 'Health & Beauty',
	'Medical': 'Health & Recovery',
	'Optics': 'Eyewear & Optics',
	'Vitamins & Supplements': 'Vitamins & Supplements',
	'Sporting & Exercise': 'Sporting & Exercise',
	'Sports Fan Gifts': 'For Sports Fans',
	'Outdoors': 'Outdoors',
	'Automotive & Motorcycle': 'Automotive Parts and Accessories',
	'Electronics': 'Electronics',
	'Gadgets & Gifts': 'Gifts & Gadgets',
	'Office Supplies & School': 'Office & School Supplies',
	'Educational': 'Office Supplies & School',
	'Pet Supplies': 'Pet Supplies',
	'Baby & Toddler': 'Baby & Kids',
	'Toys & Games': 'Toys, Games & Hobbies',
	'Apparel & Clothing': 'Fashion',
	'Shoes & Boots': 'Boots & Shoes',
	'Eyewear': 'Eyewear & Optics',
	'Travel & Bags': 'Bags, Luggage & Travel Gear',
	'Computers & Networking': 'Computers & Networking',
	'Telecommunication': 'Vintage Telecommunication',
	'Arts & Crafts': 'Arts, Crafts & DIYs',
	'Adults Only': 'Adults Only',
	'Cell Phones & Accessories': 'Cell Phones & Accessories',
	'Costumes & Props': 'Costumes & Props',
	'Occult & Magical': 'Mystic & Charming',
	'Fragrance & Perfume': 'Fragrance & Perfume',
	'General Merchandise': 'General Merchandise',
	'Security & Safety': 'Safety & Security',
	'Marine & Boating': 'Marine & Boating',
	'Seasonal & Special Occasions': 'Festive Occasions',
	'Tools & Hardware': 'Tools & Hardware',
	'Knives & Multi-tools': 'Knives & Multi-Tools',
	'Accessories': 'General Merchandise',
	'Grocery': 'Groceries & Whole Foods',
	'Hobbies': 'Toys, Games & Hobbies',
	'Home Improvement': 'Home Improvement',
	'Home, Garden & Furniture': 'Home, Garden & Furniture',
	'Jewelry': 'Jewelry',
	'Kitchen': 'Kitchen & Appliances',
	'Musical Instruments': 'Musical Instruments',
	'Watches': 'Watches',
	'Books & Videos': 'Office & School Supplies',
	'Bulk Accessories': 'General Merchandise',
}

obyshi_category_mapping = {
	'Health & Beauty': 7, 'Health & Recovery': 8, 'Vitamins & Supplements': 12, 'Sporting & Exercise': 14,
	'Automotive Parts and Accessories': 16, 'Electronics': 17, 'Office & School Supplies': 19, 'Pet Supplies': 20,
	'Baby & Kids': 21, 'Fashion': 26, 'Arts, Crafts & DIYs': 28, 'Adults Only': 29, 'Cell Phones & Accessories': 30,
	'Costumes & Props': 31, 'Fragrance & Perfume': 32, 'General Merchandise': 33, 'Groceries & Whole Foods': 34,
	'Toys, Games & Hobbies': 35, 'Home Improvement': 36, 'Home, Garden & Furniture': 37, 'Jewelry': 38,
	'Kitchen & Appliances': 39, 'Musical Instruments': 40, 'Watches': 41, 'Mystic & Charming': 43,
	'Computers & Networking': 45, 'Eyewear & Optics': 47, 'Festive Occasions': 48, 'Marine & Boating': 49,
	'Knives & Multi-Tools': 50, 'Bags, Luggage & Travel Gear': 51, 'Boots & Shoes': 52, 'Vintage Telecommunication': 53,
	'Outdoors': 54, 'Gifts & Gadgets': 55, 'For Sports Fans': 56, 'Safety & Security': 57, 'Tools & Hardware': 58

}

# Replacing wholesale2b category names with obyshi category names and then ids.
new_dataframe['CategoryId'] = new_dataframe['CategoryId'].replace(wholesale2b_to_obyshi_dictionary)
new_dataframe['CategoryId'] = new_dataframe['CategoryId'].replace(obyshi_category_mapping)

# Filling empty cells with zeros.
cells_to_zero = [
	"Brand", "CategoryId", "SubcategoryId", "ChildcategoryId", "Manufacturer", "ProductType"
]

cell_replacements = {cell: 0 for cell in cells_to_zero}
new_dataframe.fillna(cell_replacements, inplace=True)

# Making some columns zeros.
columns_to_zero = [
	"Brand", "SubcategoryId", "ChildcategoryId", "Manufacturer", "ProductType", "IsTopDeals", "IsTodaysDeals",
	"IsBulkProduct", "MinimumBulk", "MaximumBulk"
]
new_dataframe.loc[:, columns_to_zero] = 0

# Making some columns ones.
columns_to_one = ["Unit", "IsDropshipping", "Status", "Type"]
new_dataframe.loc[:, columns_to_one] = 1

# Converting : to = in the Attribute column.
new_dataframe['Attribute'] = new_dataframe['Attribute'].apply(lambda x: x.replace(':', '=') if isinstance(x, str) else x)

#ALTERNATIVE
# for i in new_dataframe.index: 
# 	new_dataframe.loc[i, 'Attribute'] = str(new_dataframe.loc[i, 'Attribute']).replace(':', '=')

# Removing the special characters in the new 'Attributes' column.
# new_dataframe['Attribute'] = new_dataframe['Attribute'].map(str).apply(lambda x: x.encode('utf-8').decode('ascii', 'ignore'))
new_dataframe = new_dataframe.replace(to_replace=['\n', '\t', '\r', '$', '@', '^'], value='', regex=True)



def splitting_dataframe_into_files():
	rows_per_file = 1000

	# Making sure the 'rows_per_file' variable is an integer
	if not isinstance(rows_per_file, int):
		raise ValueError("rows_per_file must be an integer")

	number_of_files_needed = len(new_dataframe) // rows_per_file + (len(new_dataframe) % rows_per_file > 0)

	new_dataframe_list = [
		new_dataframe.iloc[i:i + rows_per_file].copy() for i in range(0, len(new_dataframe), rows_per_file)
	]

	# Creating the output directory if it does not exist.
	output_directory = rf"output_files"

	try:
		os.mkdir(output_directory)
	except OSError as error:
		print(error)
	except FileExistsError as error: 
		print(f'File exists: {error}')

	# Writing the dataframe to a .csv file.
	for i, smaller_df in enumerate(new_dataframe_list):
		smaller_df.to_csv(f"output_files/attributes_file_{i + 1}.csv", index=False, encoding='utf-8')


splitting_dataframe_into_files()
