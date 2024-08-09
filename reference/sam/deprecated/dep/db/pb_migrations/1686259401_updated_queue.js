migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "afmmyeka",
    "name": "artists",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // remove
  collection.schema.removeField("afmmyeka")

  return dao.saveCollection(collection)
})
