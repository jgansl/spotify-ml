migrate((db) => {
  const collection = new Collection({
    "id": "z9au39tr0nexp2j",
    "created": "2023-09-08 17:25:57.164Z",
    "updated": "2023-09-08 17:25:57.164Z",
    "name": "playlists",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "ppgjezun",
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
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("z9au39tr0nexp2j");

  return dao.deleteCollection(collection);
})
