migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "mhxggf6n",
    "name": "release_date_str",
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
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "mhxggf6n",
    "name": "release_year_str",
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
