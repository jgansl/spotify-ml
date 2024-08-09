migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "1m8xlzuk",
    "name": "channel",
    "type": "text",
    "required": false,
    "unique": false,
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
  collection.schema.removeField("1m8xlzuk")

  return dao.saveCollection(collection)
})
