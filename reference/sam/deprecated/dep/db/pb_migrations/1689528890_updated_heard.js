migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "0lla4bvf",
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
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i")

  // remove
  collection.schema.removeField("0lla4bvf")

  return dao.saveCollection(collection)
})