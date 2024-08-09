migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "hgduvins",
    "name": "release_date",
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
  collection.schema.removeField("hgduvins")

  return dao.saveCollection(collection)
})
