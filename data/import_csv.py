import csv
import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://dynamodb-local:8000")
client = dynamodb.meta.client
# Reference to your DynamoDB table
table_name = 'ProjectHours'

# Check if table exists
existing_tables = client.list_tables()['TableNames']

if table_name not in existing_tables:
    # Create the table with a GSI
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'year_month',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'project_name',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year_month',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'project_name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[  # Specify the GSI details
            {
                'IndexName': 'YearMonthIndex',  # Your chosen GSI name
                'KeySchema': [
                    {
                        'AttributeName': 'year_month',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'  # You can choose a different projection type if needed
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )

    print("Created table with GSI.")
    table.wait_until_exists()

else:
    print("Table already exists.")

table = dynamodb.Table(table_name)

# Path to your CSV file
csv_file = 'data/projects.csv'

with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:  # Specify 'utf-8-sig' encoding
    reader = csv.DictReader(csvfile)
    for row in reader:
        project_name = row['project_name']
        hours = int(row['hours'])
        year_month = row['year_month']
        
        # Insert the data into DynamoDB
        table.put_item(
            Item={
                'project_name': project_name,
                'hours': hours,
                'year_month': year_month
            }
        )

print(f'Data from {csv_file} has been imported to {table_name}.')
