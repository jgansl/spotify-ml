migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "3zmsq8n1",
    "name": "owner_name",
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
  collection.schema.removeField("3zmsq8n1")

  return dao.saveCollection(collection)
})
