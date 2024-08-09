migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "rl3nx2r7",
    "name": "artists",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i")

  // remove
  collection.schema.removeField("rl3nx2r7")

  return dao.saveCollection(collection)
})
