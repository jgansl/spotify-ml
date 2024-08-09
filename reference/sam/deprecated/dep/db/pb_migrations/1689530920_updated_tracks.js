migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "sdih0v1r",
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
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // remove
  collection.schema.removeField("sdih0v1r")

  return dao.saveCollection(collection)
})
