migrate((db) => {
  const collection = new Collection({
    "id": "ozirxi4mc7sfy1b",
    "created": "2023-12-04 23:19:38.239Z",
    "updated": "2023-12-04 23:19:38.239Z",
    "name": "heard",
    "type": "base",
    "system": false,
    "schema": [
      {
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
  const collection = dao.findCollectionByNameOrId("ozirxi4mc7sfy1b");

  return dao.deleteCollection(collection);
})
