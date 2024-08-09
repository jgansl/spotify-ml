migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "fmy9tymk",
    "name": "genres_str",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // remove
  collection.schema.removeField("fmy9tymk")

  return dao.saveCollection(collection)
})
