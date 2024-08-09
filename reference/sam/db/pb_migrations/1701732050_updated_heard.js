migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ozirxi4mc7sfy1b")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "hkmcfltx",
    "name": "release_date",
    "type": "date",
    "required": false,
    "unique": false,
    "options": {
      "min": "",
      "max": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ozirxi4mc7sfy1b")

  // remove
  collection.schema.removeField("hkmcfltx")

  return dao.saveCollection(collection)
})
