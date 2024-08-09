migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "wej2t8w2",
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
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf")

  // remove
  collection.schema.removeField("wej2t8w2")

  return dao.saveCollection(collection)
})
