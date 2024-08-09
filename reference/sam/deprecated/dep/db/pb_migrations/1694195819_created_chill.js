migrate((db) => {
  const collection = new Collection({
    "id": "vzbq6nqyi8wktwe",
    "created": "2023-09-08 17:56:59.730Z",
    "updated": "2023-09-08 17:56:59.730Z",
    "name": "chill",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "ziqsllvx",
        "name": "sid",
        "type": "text",
        "required": false,
        "unique": false,
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
  const collection = dao.findCollectionByNameOrId("vzbq6nqyi8wktwe");

  return dao.deleteCollection(collection);
})
