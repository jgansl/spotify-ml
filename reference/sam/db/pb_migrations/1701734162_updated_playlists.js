migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "otwdhfab",
    "name": "description",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "cbzss0pa",
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
  const collection = dao.findCollectionByNameOrId("g2skj8b365ba8iq")

  // remove
  collection.schema.removeField("otwdhfab")

  // remove
  collection.schema.removeField("cbzss0pa")

  return dao.saveCollection(collection)
})
