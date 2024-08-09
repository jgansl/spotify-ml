migrate((db) => {
  const collection = new Collection({
    "id": "yr1scshln5zf46m",
    "created": "2023-09-08 17:29:29.925Z",
    "updated": "2023-09-08 17:29:29.925Z",
    "name": "cache",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "qvyald8s",
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
  const collection = dao.findCollectionByNameOrId("yr1scshln5zf46m");

  return dao.deleteCollection(collection);
})
