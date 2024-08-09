migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "5ab3etzn",
    "name": "date_added",
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
  collection.schema.removeField("5ab3etzn")

  return dao.saveCollection(collection)
})
