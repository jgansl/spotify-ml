migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "7tsqr28t",
    "name": "genres",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // remove
  collection.schema.removeField("7tsqr28t")

  return dao.saveCollection(collection)
})
