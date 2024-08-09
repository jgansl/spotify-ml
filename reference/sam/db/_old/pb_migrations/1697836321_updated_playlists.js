migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "1ymoxizb",
    "name": "channel",
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
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  // remove
  collection.schema.removeField("1ymoxizb")

  return dao.saveCollection(collection)
})
