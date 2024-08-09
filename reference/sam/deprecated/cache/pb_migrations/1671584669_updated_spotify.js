migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "xjjj2hyq",
    "name": "genres",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ni0xd57a",
    "name": "attributes",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  // remove
  collection.schema.removeField("xjjj2hyq")

  // remove
  collection.schema.removeField("ni0xd57a")

  return dao.saveCollection(collection)
})
