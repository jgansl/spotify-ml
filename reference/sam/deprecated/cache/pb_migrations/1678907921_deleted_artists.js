migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("yhulybbd3fjzqax");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "yhulybbd3fjzqax",
    "created": "2022-12-21 17:16:49.308Z",
    "updated": "2023-01-15 15:20:46.028Z",
    "name": "artists",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "vyk1jfgo",
        "name": "sid",
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
        "id": "fvlxv8c0",
        "name": "genres",
        "type": "json",
        "required": false,
        "unique": false,
        "options": {}
      },
      {
        "system": false,
        "id": "1to7vkh6",
        "name": "tracks",
        "type": "json",
        "required": false,
        "unique": false,
        "options": {}
      }
    ],
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
})
