migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "4kqs5agn",
    "name": "history",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // remove
  collection.schema.removeField("4kqs5agn")

  return dao.saveCollection(collection)
})
