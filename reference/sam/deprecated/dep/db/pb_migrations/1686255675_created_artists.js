migrate((db) => {
  const collection = new Collection({
    "id": "fs55uhgynzes8e4",
    "created": "2023-06-08 20:21:15.620Z",
    "updated": "2023-06-08 20:21:15.620Z",
    "name": "artists",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "pd9ikf1u",
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
  const collection = dao.findCollectionByNameOrId("fs55uhgynzes8e4");

  return dao.deleteCollection(collection);
})
