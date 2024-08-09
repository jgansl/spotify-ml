migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "eovs6keh",
    "name": "playcount",
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
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "eovs6keh",
    "name": "playcount",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
})
