from preprocess_data import save_multiband
from create_datacube import create_datacube
from generate_stac_catalog import generate_stac_catalog
from query_stac_catalog import query_stac_catalog

def main():
    print("Starting the data processing pipeline...\n")

    # Step 1: Preprocess and save the multiband raster
    print("Step 1: Preprocessing and saving the multiband raster...")
    save_multiband()

    # Step 2: Create the geospatial datacube
    print("\nStep 2: Creating the geospatial datacube...")
    create_datacube()

    # Step 3: Generate the STAC catalog
    print("\nStep 3: Generating the STAC catalog...")
    generate_stac_catalog()

    # Step 4: Query the STAC catalog (optional)
    print("\nStep 4: Querying the STAC catalog...")
    catalog_path = "C:/Users/LOCATEG5/amini_technical_assignment/data/processed/test2/stac_catalog/catalog.json"
    items = query_stac_catalog(catalog_path)

    print(f"\nFound {len(items)} STAC items:")
    for item in items:
        print(f" - {item.id}")

    print("\nPipeline execution complete. ✅")

if __name__ == "__main__":
    main()