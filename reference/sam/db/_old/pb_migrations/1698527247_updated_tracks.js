migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // remove
  collection.schema.removeField("kofqsry1")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "c9zz2i7t",
    "name": "playlists",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "kofqsry1",
    "name": "playlists",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // remove
  collection.schema.removeField("c9zz2i7t")

  return dao.saveCollection(collection)
})
