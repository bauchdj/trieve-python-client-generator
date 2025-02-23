from oxide_client.src.oxide_region_api import OxideRegionAPI

# Create SDK instance
sdk = OxideRegionAPI()


def main():
    # random oxide handler
    sdk.images.image_create()


if __name__ == "__main__":
    main()
