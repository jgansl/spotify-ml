migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "d8iwi26f",
    "name": "specificity",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  // remove
  collection.schema.removeField("d8iwi26f")

  return dao.saveCollection(collection)
})
