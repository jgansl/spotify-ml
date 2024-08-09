migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "4jlxrnws",
    "name": "uri",
    "type": "text",
    "required": false,
    "unique": true,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("w6zm9hujt26288n")

  // remove
  collection.schema.removeField("4jlxrnws")

  return dao.saveCollection(collection)
})
