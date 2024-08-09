migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "d1wcfetr",
    "name": "owner",
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
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  // remove
  collection.schema.removeField("d1wcfetr")

  return dao.saveCollection(collection)
})
