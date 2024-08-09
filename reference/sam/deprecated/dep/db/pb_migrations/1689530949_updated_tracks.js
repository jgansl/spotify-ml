migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "dyancyx1",
    "name": "artists",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "lbjwgnwp",
    "name": "sid",
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
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy")

  // remove
  collection.schema.removeField("dyancyx1")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "lbjwgnwp",
    "name": "sid",
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
})
