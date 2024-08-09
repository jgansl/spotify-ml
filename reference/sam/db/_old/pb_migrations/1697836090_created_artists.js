migrate((db) => {
  const collection = new Collection({
    "id": "xpo6rzgjkk2gwnj",
    "created": "2023-10-20 21:08:10.507Z",
    "updated": "2023-10-20 21:08:10.507Z",
    "name": "artists",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "uglajhjk",
        "name": "spotify_id",
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
  const collection = dao.findCollectionByNameOrId("xpo6rzgjkk2gwnj");

  return dao.deleteCollection(collection);
})
