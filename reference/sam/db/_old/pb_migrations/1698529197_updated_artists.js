migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "caxvclng",
    "name": "popularity",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "2ywijqzm",
    "name": "followers",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // remove
  collection.schema.removeField("caxvclng")

  // remove
  collection.schema.removeField("2ywijqzm")

  return dao.saveCollection(collection)
})
