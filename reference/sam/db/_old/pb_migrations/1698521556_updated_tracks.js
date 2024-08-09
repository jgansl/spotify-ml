migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "tzk1y0rw",
    "name": "liked",
    "type": "bool",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // remove
  collection.schema.removeField("tzk1y0rw")

  return dao.saveCollection(collection)
})
