migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("2iktfdxdqfbl65x")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "fynytq0j",
    "name": "name",
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
  const collection = dao.findCollectionByNameOrId("2iktfdxdqfbl65x")

  // remove
  collection.schema.removeField("fynytq0j")

  return dao.saveCollection(collection)
})
