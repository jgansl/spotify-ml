migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qiaqk4xh",
    "name": "genre",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "8en2eub7",
    "name": "new",
    "type": "bool",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos")

  // remove
  collection.schema.removeField("qiaqk4xh")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "8en2eub7",
    "name": "heard",
    "type": "bool",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
})
