migrate((db) => {
  const collection = new Collection({
    "id": "sbf05w0cbsaspos",
    "created": "2023-12-05 22:56:59.752Z",
    "updated": "2023-12-05 22:56:59.752Z",
    "name": "tracks",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "owvt0tki",
        "name": "spotify_id",
        "type": "text",
        "required": true,
        "unique": true,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "9j21brzz",
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
  const collection = dao.findCollectionByNameOrId("sbf05w0cbsaspos");

  return dao.deleteCollection(collection);
})
