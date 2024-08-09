migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ozirxi4mc7sfy1b")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "atq6zd5t",
    "name": "name",
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
    "id": "va69kohw",
    "name": "popularity",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qf2y4xpz",
    "name": "sid",
    "type": "text",
    "required": true,
    "unique": true,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ozirxi4mc7sfy1b")

  // remove
  collection.schema.removeField("atq6zd5t")

  // remove
  collection.schema.removeField("va69kohw")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qf2y4xpz",
    "name": "sid",
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
