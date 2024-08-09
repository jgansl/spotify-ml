migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("bszklb23jxrrv02")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ef26kzoi",
    "name": "artist_genres",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qnueeiyg",
    "name": "genre_mix",
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
  const collection = dao.findCollectionByNameOrId("bszklb23jxrrv02")

  // remove
  collection.schema.removeField("ef26kzoi")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qnueeiyg",
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

  return dao.saveCollection(collection)
})
