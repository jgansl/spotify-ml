migrate((db) => {
  const collection = new Collection({
    "id": "8p5rvogva06xyu4",
    "created": "2023-10-20 22:03:16.847Z",
    "updated": "2023-10-20 22:03:16.847Z",
    "name": "meta",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "oecohf7h",
        "name": "last_run",
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
  const collection = dao.findCollectionByNameOrId("8p5rvogva06xyu4");

  return dao.deleteCollection(collection);
})
