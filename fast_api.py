"""
4 major methods for any API

GET : asking for information
PUT : Update information
POST : sending information to the server/creating a information
DELETE: Deleting modification
uvicorn fast_api:app --reload
uvicorn <pyname>:app --reload
"""
from fastapi import FastAPI, Query, Path, HTTPException, status
from typing import Optional # for optional paramters
from pydantic import BaseModel # creation of an object and the fetching items.

inventory={1:{"name":"keyboard","price":300,"brand":"dell"},2:{"name":"mouse","price":200,"brand":"dell"}}

class item_details(BaseModel):
	name: str
	price: int
	brand: Optional[str]=None

app=FastAPI()
#creation of the home page
@app.get("/")
def home():
	return {"Data":"Hello world"} # will be converted to jsaon data.
#fast will convert this to json data. hence we can use python data type.
#even while recieving data, the data is recieved in jason and this will be converted
#to python data type by fastapi

#creation of a new page
@app.get("/about")
def about():
	return ("this is an example page")

# passing parameters
@app.get("/get-item/{item_id}")
#@app.get("/get-item/{item_id}/{param2}") # passing items with multiple parameters
def get_item(item_id:int):
 return inventory[item_id]

#adding doc strings
@app.get("/get-item-description/{item_id}/{descr}")
def get_item_description(item_id:int,descr:str ):
	return inventory[item_id]

#adding validations
@app.get("/getitem/{item_id}")
def getitem(item_id:int = Path(1,description="pass out value",gt=0)):
		return inventory[item_id]

#optional paramters for querying data
@app.get("/get-item-optional/{item_id}")
def get_item_optional(item_id:Optional[int]=None):
	if item_id is None or item_id=='':
		#return('invalid')
		return inventory
	else:
		return inventory[item_id]

@app.post("/create_item/{item_id}")
def create_item(item_id:int, itemdet:item_details):
	if item_id in inventory:
		return("item already exists")
	else:
		#inventory[item_id]={"name":itemdet.name,"price":itemdet.price,"brand":itemdet.brand}
		 inventory[item_id]=itemdet
	return inventory[item_id]

@app.put("/update_item/{item_id}")
def update_item(item_id:int,itemdet:item_details):
	if item_id in inventory:
		inventory[item_id] = itemdet
		return inventory[item_id]
	else:
		#inventory[item_id]={"name":itemdet.name,"price":itemdet.price,"brand":itemdet.brand}
		return ("item does not exists")

@app.delete("/delete-item/{item_id}")
def delete_item(item_id:int = Query(...,description="to delete an item",ge=0)):
	if item_id in inventory:
		del inventory[item_id]
		return inventory
	else:
		raise HTTPException(status_code=404,detail="item id not found")
		#return ("item id does not exist")
