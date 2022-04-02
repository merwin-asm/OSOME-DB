
# OsomeDB 1.0.3

Make And Manage DBs in Python.



## Installation

Install OsomeDB with pip

```bash
  pip install OsomeDB
```
    
## Features

- Cross platform (i think)
- Encryption (AES)
- Compression
- PassBin
- Examples provided

## Structure and Working

### Structure of DATA :
   
    DB - > Collections - > Docs - > DATA

### Structure of Files :
    - >  Folder(DB_NAME)
        - > File(Collection-1)
        - > File(Collection-2)
        - > File(Collection-3)
        - > Config.json
        - > PassBin-1(Created When There is a request for saving passwords)
### Config File (json) :
    - > DB_NAME
    - > Date Created
    - > List of collections
    - > enc
    Eg : {"DB_NAME":"A","CREATED":"","COLLECTIONS":["A","B","C"],"ENC":false}
### PassBin (json):
    Eg : {"Id":"Guy-1","Password":"The Guy's Password"}



## Usage/Examples

```python
from OsomeDB import OsomeDB
# Create/Get DB
"""
  If No DB exists in db_path a new one will be created
    :param db_path: Path to the DB
"""
DB = OsomeDB("School") 
```

### Note : To Enable encryption from the code,
```python
# changing the settings
DB.Settings("School").change("ENC","HERE PUT THE ENCRYTION KEY") # Turning on encryption
```
or edit the config.json file.


DB class:
```python
  len(DB) # returns num of collections
  DB.__sizeof__() # returns the size of the DB
  DB += "NewStudents" # makes a new collection
  DB -= "NewStudents" # deletes the collection
  DB.collection_exists("NewStudents") # checks if a collection exists
  DB.make_collection("NewStudents") # makes a collection
  DB.date_created() # returns the date when the DB was created
  DB.get_collection("NewStudents") # returns a Obj of class Collection
  DB.remove_collection("Collection-B") # deletes the collection
  DB.total_collections() # returns the number of collections
  DB.total_docs() # returns the number of Docs in the DB
  DB.get_db_size() # returns the size of the DB
  DB.get_db_collections() # returns all collections (name)
  DB.get_settings() # returns settings
  DB.write_settings(new_settings) # rewrites the settings
  DB.renew_db() # Renews the DB with the new config file
  DB.load_collection() # returns the collection data
  DB.write_collection(New_collection_data) # rewrites collection data
  DB.delete_collection() # deletes a collection
  DB.get_collection_size() # returns the size of a collection
```

Collection class:
```python
  from OsomeDB import Collection
  collection = Collection("School","Students") # path to DB , Collection name
  # or
  collection = DB.get_collection("Students")
  len(collection) # returns the number of Docs in the Collection
  new_collection = collection+{"rollno.":1,"student":"Merwin"} # adds a doc
  new_collection = collection-{"rollno.":1,"student":"Merwin"} # removes a doc
  collection+={"rollno.":1,"student":"Merwin"} # adds a doc and saves
  collection-={"rollno.":1,"student":"Merwin"} # removes a doc and saves
  collection.delete() # deletes the collection
  collection.__sizeof__() # returns the size of the collection
  collection.read_collection_data() # returns the collection data
  collection.rewrite_collection_data() # rewrites the collection data
  collection.get_indexof({"User":user,"Id":Id etc...}) # returns the index of the data
  collection.get_byindex(1) # gets a doc by index
  # returns (index , Doc) 
  collection.search_by_key_val(key_name="Username",username) # Search using the value of a given key 
  collection.rewrite_doc(index=2,new_data={"User":user,"Id":Id etc...}) # rewrites a doc

```

PassBin class:
```python
   # If passbin was not found a new one will be created
   passbin  = DB.PassBin("School","passwords") # param path to DB and PassBins name.
   passbin.passbin_exists("passwords-staff") # checks if a passbin exists.
   passbin.get_pass_bin() # returns the data in passbin
   passbin.write_pass_bin(new_pass_bin_data) # rewrites the passbin
   len(passbin) # the number of passwords
   new_passbin = passbin+{"Id":Id,"Password":"passs"} # adds
   new_passbin = passbin-{"Id":Id,"Password":"passs"} # removes
   passbin = passbin+={"Id":Id,"Password":"passs"} # adds the pass and save to passbin returns passbin obj
   passbin = passbin-={"Id":Id,"Password":"passs"} # removes the pass and save to passbin returns passbin obj
```
### Note : The format to + , - , += , -= In PassBin
```
{"Id":"","Password":""}
```
```python
   passbin.delete_bin() # deletes the passbin
   passbin.get_passbin_size() # returns the size of the passbin
   passbin.__sizeof__() # returns the size of the passbin
   passbin.append_new_pass(Id="1",Password="Cooldudescave123") # Appends a new password
   passbin.remove(Id="1") # removes a password from passbin
   passbin.reset_pass(Id="2",Password="Newcoolpassword") # resets a password
   passbin.search_by_Id(Id="2") # search using the Id 
```

Settings class:
```python
   # Arg The path of the DB
   settings = DB.Settings("School") 
   settings.change(key="ENC",value=True) # changes settings
   settings.give_setting_info() # returns all keys available
   settings.get(key="ENC") # returns value of ENC
   settings.get_settings() # returns the settings
   settings.write_settings(new_settings) # rewrites the settings
```


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@Merwin](https://www.github.com/mastercodermerwin)

