migrate((db) => {
  const collection = new Collection({
    "id": "2iktfdxdqfbl65x",
    "created": "2023-03-15 19:18:53.821Z",
    "updated": "2023-03-15 19:18:53.821Z",
    "name": "artists",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "v8teym5h",
        "name": "sid",
        "type": "text",
        "required": true,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      }
    ],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("2iktfdxdqfbl65x");

  return dao.deleteCollection(collection);
})
