migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ouyqxq90",
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
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4")

  // remove
  collection.schema.removeField("ouyqxq90")

  return dao.saveCollection(collection)
})
