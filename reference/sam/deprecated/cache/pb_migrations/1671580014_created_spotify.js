migrate((db) => {
  const collection = new Collection({
    "id": "yguxfq91ip5me0u",
    "created": "2022-12-20 23:46:54.867Z",
    "updated": "2022-12-20 23:46:54.867Z",
    "name": "spotify",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "1qrk4djp",
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
        "id": "eovs6keh",
        "name": "playcount",
        "type": "number",
        "required": true,
        "unique": false,
        "options": {
          "min": null,
          "max": null
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
  const collection = dao.findCollectionByNameOrId("yguxfq91ip5me0u");

  return dao.deleteCollection(collection);
})
