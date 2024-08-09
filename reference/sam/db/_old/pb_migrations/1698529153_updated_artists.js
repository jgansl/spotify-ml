migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "n0vyhllp",
    "name": "name",
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
  collection.schema.removeField("n0vyhllp")

  return dao.saveCollection(collection)
})
