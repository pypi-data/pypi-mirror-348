import logging
import requests
from inspect import getframeinfo, stack

logger = logging.getLogger(__name__)

def get_published_products(
    shop, count=25, with_additional_fields=False, sort_key="TITLE", api_version="2023-07"
):
    '''
    Retrieves published products from a Shopify store using the GraphQL API.

    Args:
        shop (dict): Dictionary containing shop authentication details:
                    - name: The shop's domain (e.g., "your-store.myshopify.com")
                    - token: The access token for API authentication
        count (int): Maximum number of products to retrieve (default: 25)
        with_additional_fields (bool): Whether to include extra product details (default: False)
        sort_key (str): Field to sort products by (default: "TITLE")
        api_version (str): Shopify API version to use (default: "2023-07")

    Returns:
        tuple: (total_count, products_list) where:
            - total_count is the total number of published products in the store
            - products_list is a list of product objects with requested fields
    '''
    from itertools import islice

    originalcaller = getframeinfo(stack()[1][0])
    logger.info(
        'In get_published_products called from %s:%s(%d). ',
        originalcaller.filename.split('/')[-1],
        originalcaller.function,
        originalcaller.lineno,
    )

    shop_name = shop["name"]
    SHOPIFY_API_URL = (
        'https://{store_name}/admin/api/{api_version}/graphql.json'
    ).format(store_name=shop_name, api_version=api_version)

    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': shop["token"],
    }
    
    # Define additional fields to fetch if requested
    extra_fields = ''
    if with_additional_fields:
        extra_fields = '''
            totalInventory
            onlineStorePreviewUrl
            description
            priceRangeV2 {
                minVariantPrice {
                    amount
                    currencyCode
                }
                maxVariantPrice {
                    amount
                    currencyCode
                }
            }
        '''
    
    # Set fetch limit for each API call (max 250 per Shopify's limits)
    fetch_limit = min(count, 250)
    
    query = f'''
        query ($cursor: String, $fetchLimit: Int!) {{
            productsCount(query: "published_at:*") {{
                count
            }}
            products(first: $fetchLimit, after: $cursor, query: "published_at:*", sortKey: {sort_key}) {{
                edges {{
                    cursor
                    node {{
                        id
                        title
                        handle
                        publishedAt
                        {extra_fields}
                    }}
                }}
                pageInfo {{
                    hasNextPage
                }}
            }}
        }}
    '''

    published_products = []
    published_count = 0
    cursor = None

    try:
        while True:
            variables = {"cursor": cursor, "fetchLimit": fetch_limit}

            response = requests.post(
                SHOPIFY_API_URL,
                json={'query': query, 'variables': variables},
                headers=headers,
            )

            if response.status_code != 200:
                logger.error(
                    '%s: Failed to fetch data, status code: %s, message: %s',
                    shop_name,
                    response.status_code,
                    response.text,
                )
                return None, None

            response_data = response.json()

            if 'errors' in response_data:
                logger.error(
                    '%s: Errors in response data. Returning None. Errors: %s',
                    shop_name,
                    response_data['errors'],
                )
                return None, None

            published_count = response_data['data']['productsCount']['count']
            product_data = response_data['data']['products']['edges']
            page_info = response_data['data']['products']['pageInfo']

            published_products.extend([edge['node'] for edge in product_data])

            # Stop pagination if we've reached the requested count or there are no more pages
            if len(published_products) >= count:
                break
            if not page_info['hasNextPage']:
                break

            cursor = product_data[-1]['cursor']

        # Return only the requested number of products
        return published_count, list(islice(published_products, count))

    except Exception as e:
        logger.error(
            '%s: Error while retrieving the published products: %s',
            shop_name,
            e,
        )
        return None, None