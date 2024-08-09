migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "pqc1apdl",
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
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j")

  // remove
  collection.schema.removeField("pqc1apdl")

  return dao.saveCollection(collection)
})
