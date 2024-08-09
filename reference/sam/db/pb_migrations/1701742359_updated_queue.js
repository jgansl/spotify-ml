migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ejqshd8a",
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
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf")

  // remove
  collection.schema.removeField("ejqshd8a")

  return dao.saveCollection(collection)
})
