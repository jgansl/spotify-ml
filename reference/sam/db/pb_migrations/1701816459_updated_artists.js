migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n7yz6jcyo39vzn1")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ev9hus87",
    "name": "genres",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "zth3kj9t",
    "name": "genres_obj",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n7yz6jcyo39vzn1")

  // remove
  collection.schema.removeField("ev9hus87")

  // remove
  collection.schema.removeField("zth3kj9t")

  return dao.saveCollection(collection)
})
