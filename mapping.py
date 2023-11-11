# importing necessary python packages.
import pandas as pd
from fuzzywuzzy import process
import re

# Load the .csv file exported from wholesale2b.com
wholesale2b_dataframe = pd.read_csv(r"all (5).csv")

print(set(wholesale2b_dataframe['w2b_category_1']))

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
                  'description': 'Description', }

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
	'Baby & Kids' 'Fashion', 'Digital Product', 'Arts & Crafts', 'Adults Only', 'Cell Phones & Accessories',
	'Costumes & Props', 'Fragrance & Perfume', 'General Merchandise', 'Grocery', 'Games & Hobbies',
	'Home Improvement', 'Home, Garden & Furniture', 'Jewelry', 'Kitchen', 'Musical Instruments', 'Watches',
	'Mystic & Charming'
]

wholesale2b_to_obyshi_dictionary = {
	'Health & Beauty': 'Health & Beauty',
	'Medical': 'Health & Recovery',
	'Optics': 'Health & Recovery',
	'Vitamins & Supplements': 'Vitamins & Supplements',
	'Sporting & Exercise': 'Sports & Outside',
	'Sports Fan Gifts': 'Sports & Outside',
	'Outdoors': 'Sports & Outside',
	'Automotive & Motorcycle': 'Automotive',
	'Electronics': 'Electronics',
	'Gadgets & Gifts': 'Electronics',
	'Office Supplies & School': 'Office Supplies & School',
	'Educational': 'Office Supplies & School',
	'Pet Supplies': 'Pet Supplies',
	'Baby & Toddler': 'Baby & Kids',
	'Toys & Games': 'Baby & Kids',
	'Apparel & Clothing': 'Fashion',
	'Shoes & Boots': 'Fashion',
	'Eyewear': 'Fashion',
	'Travel & Bags': 'Fashion',
	'Computers & Networking': 'Digital Product',
	'Telecommunication': 'Digital Product',
	'Arts & Crafts': 'Arts & Crafts',
	'Adults Only': 'Adults Only',
	'Cell Phones & Accessories': 'Cell Phones & Accessories',
	'Costumes & Props': 'Costumes & Props',
	'Occult & Magical': 'Mystic & Charming',
	'Fragrance & Perfume': 'Fragrance & Perfume',
	'General Merchandise': 'General Merchandise',
	'Security & Safety': 'General Merchandise',
	'Marine & Boating': 'General Merchandise',
	'Seasonal & Special Occasions': 'General Merchandise',
	'Tools & Hardware': 'General Merchandise',
	'Knives & Multi-tools': 'General Merchandise',
	'Accessories': 'General Merchandise',
	'Grocery': 'Grocery',
	'Hobbies': 'Games & Hobbies',
	'Home Improvement': 'Home Improvement',
	'Home, Garden & Furniture': 'Home, Garden & Furniture',
	'Jewelry': 'Jewelry',
	'Kitchen': 'Kitchen',
	'Musical Instruments': 'Musical Instruments',
	'Watches': 'Watches',
}


# Loop through wholesale2b's list of category ids and find the most similar obyshi category id value.
def fuzzy_match(w2b_category_id):
	closest_match, score = process.extractOne(w2b_category_id, obyshi_category_ids)
	if score >= 50:
		return closest_match
	else:
		return w2b_category_id


# new_dataframe["CategoryId"] = new_dataframe["CategoryId"].apply(fuzzy_match)

obyshi_category_mapping = {
	'Health & Beauty': 7, 'Health & Recovery': 8, 'Vitamins & Supplements': 12, 'Athletic & Fitness': 13,
	'Sports & Outside': 14, 'Appliances': 15, 'Automotive': 16, 'Electronics': 17, 'Household Goods': 18,
	'Office Supplies & School': 19, 'Pet Supplies': 20, 'Baby & Kids': 21, 'Fashion': 26, 'Digital Product': 27,
	'Arts & Crafts': 28, 'Adults Only': 29, 'Cell Phones & Accessories': 30, 'Costumes & Props': 31,
	'Fragrance & Perfume': 32, 'General Merchandise': 33, 'Grocery': 34, 'Games & Hobbies': 35, 'Home Improvement': 36,
	'Home, Garden & Furniture': 37, 'Jewelry': 38, 'Kitchen': 39, 'Musical Instruments': 40, 'Watches': 41,
	'Mystic & Charming': 43,
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
	"IsBulkProduct", "MinimumBulk", "MaximumBulk", "Attribute"
]
new_dataframe.loc[:, columns_to_zero] = 0

# Making some columns ones.
columns_to_one = ["Unit", "IsDropshipping", "Status", "Type"]
new_dataframe.loc[:, columns_to_one] = 1


# Function to remove all special characters in string columns in the dataframe.
def remove_special_characters(text):
	if pd.api.types.is_string_dtype(text):
		return re.sub(r'[a-zA-z0-9\s]', ' ', text)
	return text


new_dataframe = new_dataframe.map(remove_special_characters)

# Writing the dataframe to a .csv file.
new_dataframe.to_csv("eleven thousand_mysticandcharming.csv", index=False, encoding='utf-8')
