import json

from python_notion_plus import NotionClient


def main():
    notion_client = NotionClient(database_id='1f622274-86ac-804c-a13a-ea6a77e6510e')

    metadata = notion_client.get_metadata()
    print(f'notion_schema: {metadata}')

    notion_title = notion_client.get_database_title()
    print(f'notion_title: {notion_title}')

    notion_properties = notion_client.get_database_properties()
    print(f'notion_properties: {notion_properties}')

    total_results = notion_client.get_total_results()
    print(f'total_results: {total_results}')

    notion_content = notion_client.get_database_content()
    print(f'notion_content: {notion_content}')
    for page in notion_content:
        properties = notion_client.format_notion_page(page)
        formatted_data = json.dumps(properties, indent=4)

        print(f'notion_page_properties: {formatted_data}')
        print()

if __name__ == '__main__':
    main()
