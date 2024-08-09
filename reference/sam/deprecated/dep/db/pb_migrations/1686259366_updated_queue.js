migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "uvno08t5",
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
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // remove
  collection.schema.removeField("uvno08t5")

  return dao.saveCollection(collection)
})
