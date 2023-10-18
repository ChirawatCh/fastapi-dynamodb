from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from boto3.dynamodb.conditions import Key
import boto3

app = FastAPI()

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://dynamodb-local:8000")
table_name = 'ProjectHours'

# Use the table
table = dynamodb.Table(table_name)
print("Table status:", table.table_status)

class Projects(BaseModel):
    project_name: str
    hours: int
    year_month: str

class UpdateProject(BaseModel):
    project_name: str = None
    hours: int = None

# Create a new entry
@app.post("/projects/", response_model=Projects)
def create_projects(projects: Projects):
    item = {
        'project_name': projects.project_name,
        'hours': projects.hours,
        'year_month': projects.year_month  
    }
    table.put_item(Item=item)
    return projects

# Update project by project_name and year-month
@app.put("/projects/")
def update_projects(project_name: str, year_month: str, project_updates: UpdateProject):
    # Get the existing item
    response = table.get_item(
        Key={
            'project_name': project_name,
            'year_month': year_month
        }
    )
    existing_item = response.get('Item')

    if existing_item is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update the fields if they are provided in the request
    if project_updates.project_name is not None:
        existing_item['project_name'] = project_updates.project_name
    if project_updates.hours is not None:
        existing_item['hours'] = project_updates.hours

    # Save the updated item back to the table
    response = table.put_item(Item=existing_item)
    if response:
        return existing_item
    else:
        raise HTTPException(status_code=404, detail="Update failed")

# Delete project by project_name and year-month
@app.delete("/projects/")
def delete_projects(project_name: str, year_month: str):
    response = table.delete_item(
        Key={
            'project_name': project_name,
            'year_month': year_month
        }
    )
    if response:
        return {"message": "Project has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="Deletion failed")
    
# Get project by project_name and year-month
@app.get("/projects/")
def read_projects(project_name: str, year_month: str):
    response = table.get_item(
        Key={
            'project_name': project_name,
            'year-month': year_month
        }
    )
    item = response.get('Item')
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Project not found")

# Get a list of unique year-month values
@app.get("/year_months/")
def get_year_months():
    response = table.scan(
        ExpressionAttributeNames={'#ym': 'year_month'},
        ProjectionExpression='#ym',
        Select="SPECIFIC_ATTRIBUTES"
    )

    items = response.get('Items', [])
    unique_year_months = set(item['year_month'] for item in items)

    return list(unique_year_months)

# Get project hours by year_month and calculate percentages
@app.get("/projects/{year_month}")
def get_monthly_projects(year_month: str):
    # Query the DynamoDB table for items with the specified year_month
    response = table.query(
        IndexName='YearMonthIndex',  # Replace with your actual index name if you have one
        KeyConditionExpression=Key('year_month').eq(year_month),
    )

    items = response.get('Items', [])

    if not items:
        raise HTTPException(status_code=404, detail=f"No data found for the specified {year_month}, string format should be like this: 2023-may")

    # Calculate the total hours for the month
    total_hours = sum(item['hours'] for item in items)

    # Calculate the percentage for each project
    result = {
        year_month: {
            "data": [],
            "Total": {
                "hours": total_hours
            }
        }
    }

    for item in items:
        percent = (item['hours'] / total_hours) * 100
        project_data = {
            "project_name": item['project_name'],
            "hours": item['hours'],
            "percent": round(percent, 2)  # Round the percentage to two decimal places
        }
        result[year_month]["data"].append(project_data)

    return result
