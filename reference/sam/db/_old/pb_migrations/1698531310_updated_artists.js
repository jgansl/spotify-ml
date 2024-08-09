migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "dkeoubzf",
    "name": "uri",
    "type": "url",
    "required": false,
    "unique": false,
    "options": {
      "exceptDomains": null,
      "onlyDomains": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj")

  // remove
  collection.schema.removeField("dkeoubzf")

  return dao.saveCollection(collection)
})
