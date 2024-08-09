migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "uxtozxjr",
    "name": "hide",
    "type": "bool",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  // remove
  collection.schema.removeField("uxtozxjr")

  return dao.saveCollection(collection)
})
