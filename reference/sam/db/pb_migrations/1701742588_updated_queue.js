migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "pup57hfx",
    "name": "release_date",
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
  const collection = dao.findCollectionByNameOrId("8g478vgl2qaz0kf")

  // remove
  collection.schema.removeField("pup57hfx")

  return dao.saveCollection(collection)
})
