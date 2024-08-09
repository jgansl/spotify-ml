migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "5wuelkjv",
    "name": "uri",
    "type": "text",
    "required": true,
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
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // remove
  collection.schema.removeField("5wuelkjv")

  return dao.saveCollection(collection)
})
