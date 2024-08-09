migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // remove
  collection.schema.removeField("ydt3o26h")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "jjdjqwbb",
    "name": "heard",
    "type": "bool",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "z7k0e7fr",
    "name": "artists",
    "type": "json",
    "required": false,
    "unique": false,
    "options": {}
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "kofqsry1",
    "name": "playlists",
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
    "id": "d3bomfkc",
    "name": "personal_year",
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
    "id": "5mcjckuv",
    "name": "release_date",
    "type": "date",
    "required": false,
    "unique": false,
    "options": {
      "min": "",
      "max": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ydt3o26h",
    "name": "playcount",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": 0,
      "max": null
    }
  }))

  // remove
  collection.schema.removeField("jjdjqwbb")

  // remove
  collection.schema.removeField("z7k0e7fr")

  // remove
  collection.schema.removeField("kofqsry1")

  // remove
  collection.schema.removeField("d3bomfkc")

  // remove
  collection.schema.removeField("5mcjckuv")

  return dao.saveCollection(collection)
})
