migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "kmh1fbpf",
    "name": "followers",
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
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4")

  // remove
  collection.schema.removeField("kmh1fbpf")

  return dao.saveCollection(collection)
})
