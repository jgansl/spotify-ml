migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "wunaost8",
    "name": "genres",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "nujezg6a",
    "name": "popularity",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "rtvx6yqq",
    "name": "heard",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "xykf7mus",
    "name": "queue",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4")

  // remove
  collection.schema.removeField("wunaost8")

  // remove
  collection.schema.removeField("nujezg6a")

  // remove
  collection.schema.removeField("rtvx6yqq")

  // remove
  collection.schema.removeField("xykf7mus")

  return dao.saveCollection(collection)
})
