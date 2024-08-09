migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("2iktfdxdqfbl65x")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "pozz2ghj",
    "name": "genres",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "esjsuprw",
    "name": "tracks",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("2iktfdxdqfbl65x")

  // remove
  collection.schema.removeField("pozz2ghj")

  // remove
  collection.schema.removeField("esjsuprw")

  return dao.saveCollection(collection)
})
