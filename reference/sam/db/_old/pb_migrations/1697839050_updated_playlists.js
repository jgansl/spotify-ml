migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qlct5xpk",
    "name": "public",
    "type": "bool",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  // remove
  collection.schema.removeField("qlct5xpk")

  return dao.saveCollection(collection)
})
