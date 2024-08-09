migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // remove
  collection.schema.removeField("nt3gm0ko")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "a3lxyvzv",
    "name": "uri",
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

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "nt3gm0ko",
    "name": "uri",
    "type": "url",
    "required": false,
    "unique": false,
    "options": {
      "exceptDomains": null,
      "onlyDomains": null
    }
  }))

  // remove
  collection.schema.removeField("a3lxyvzv")

  return dao.saveCollection(collection)
})
