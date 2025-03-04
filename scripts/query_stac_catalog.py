import pystac

def query_stac_catalog(catalog_path, collections=None):
    """
    Query the static STAC catalog stored locally.

    Args:
        catalog_path (str): Path to the root STAC catalog JSON file.
        collections (list, optional): List of collection IDs to filter items.

    Returns:
        list: List of STAC items that match the query.
    """
    catalog = pystac.Catalog.from_file(catalog_path)

    items = []
    for item in catalog.get_all_items():
        if not collections or item.collection_id in collections:  # Fixed here
            items.append(item)

    return items

# # Example usage
# catalog_path = "C:/Users/LOCATEG5/amini_technical_assignment/data/processed/test2/stac_catalog/catalog.json"
# results = query_stac_catalog(catalog_path, collections=["africa-environmental-datacube"])

# for item in results:
#     print(item.id, item.assets)