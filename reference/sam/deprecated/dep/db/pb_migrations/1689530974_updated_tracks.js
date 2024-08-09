migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "8acbept2",
    "name": "play_count",
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
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // remove
  collection.schema.removeField("8acbept2")

  return dao.saveCollection(collection)
})
