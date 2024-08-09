migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "cq5e5qo6",
    "name": "cached",
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
  collection.schema.removeField("cq5e5qo6")

  return dao.saveCollection(collection)
})
