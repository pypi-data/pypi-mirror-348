
[![PyPI](https://img.shields.io/pypi/v/pantherdb?label=PyPI)](https://pypi.org/project/pantherdb/) [![PyVersion](https://img.shields.io/pypi/pyversions/pantherdb.svg)](https://pypi.org/project/pantherdb/) [![Downloads](https://static.pepy.tech/badge/pantherdb/month)](https://pepy.tech/project/pantherdb) [![license](https://img.shields.io/github/license/alirn76/pantherdb.svg)](https://github.com/alirn76/pantherdb/blob/main/LICENSE)

## Introduction

PantherDB is a <b>Simple</b>, <b>FileBase</b> and <b>Document Oriented</b> database that you can use in your projects.

### Features:
- Document Oriented
- Easy to use
- Written in pure Python +3.8 based on standard type hints
- Handle Database Encryption
- Singleton connection per `db_name`

## Usage

### Database:
- #### Create a database:
    ```python
    db: PantherDB = PantherDB('database.pdb')
    ```
  
- #### Create an encrypted database:
    Required `cyptography` install it with `pip install pantherdb[full]`
    ```python
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()  # Should be static (You should not generate new key on every run)
    db: PantherDB = PantherDB('database.pdb', secret_key=key)
    ```

- #### Access to a collection:
    ```python
    user_collection: PantherCollection = db.collection('User')
    ```

- #### Delete a collection:
    ```python
    db.collection('User').drop()
    ```
### Create:
- #### Insert document:
    ```python
    user: PantherDocument = db.collection('User').insert_one(first_name='Ali', last_name='Rn')
    ```

### Get:
- #### Find one document:
    ```python
    user: PantherDocument = db.collection('User').find_one(first_name='Ali', last_name='Rn')
    ```
    or
    ```python
    user: PantherDocument = db.collection('User').find_one()
    ```
  
- #### Find first document (alias of `find_one()`):
    ```python
    user: PantherDocument = db.collection('User').first(first_name='Ali', last_name='Rn')
    ```
    or
    ```python
    user: PantherDocument = db.collection('User').first()
    ```
  
- #### Find last document:
    ```python
    user: PantherDocument = db.collection('User').last(first_name='Ali', last_name='Rn')
    ```
    or
    ```python
    user: PantherDocument = db.collection('User').last()
    ```
  
- #### Find documents:
    ```python
    users: list[PantherDocument] = db.collection('User').find(last_name='Rn')
    ```
    or all documents
    ```python
    users: list[PantherDocument] = db.collection('User').find()
    ```

- #### Count documents:
    ```python
    users_count: int = db.collection('User').count(first_name='Ali')
    ```

### Update:
- #### Update a document:
  ```python
  user: PantherDocument = db.collection('User').find_one(first_name='Ali', last_name='Rn')
  user.update(name='Saba')
  ```

- #### Filter and Update a document:
  ```python
  _filter = {'first_name': 'Ali', 'last_name': 'Rn'}
  is_updated: bool = db.collection('User').update_one(_filter, first_name='Saba')
  ```

- #### Filter and Update many:
  ```python
  _filter = {'first_name': 'Ali'}
  updated_count: int = db.collection('User').update_many(_filter, first_name='Saba')
  ```
  
### Delete:
- #### Delete a document:
  ```python
  user: PantherDocument = db.collection('User').first(first_name='Ali', last_name='Rn')
  user.delete()
  ```

- #### Filter and Delete a document:
  ```python
  is_deleted: bool = db.collection('User').delete_one(first_name='Ali', last_name='Rn')
  ```

- #### Filter and Delete many:
  ```python
  deleted_count: int = db.collection('User').delete_many(last_name='Rn')
  ```
  
## TODO:
- [x] Add encryption
- [ ] Complete tests TODO
- [ ] Add B+ tree
