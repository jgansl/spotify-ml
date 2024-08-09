migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "epir0tum",
    "name": "uri",
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
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  // remove
  collection.schema.removeField("epir0tum")

  return dao.saveCollection(collection)
})
