migrate((db) => {
  const collection = new Collection({
    "id": "8lb1kv0zfo0i7xy",
    "created": "2023-07-16 18:07:49.769Z",
    "updated": "2023-07-16 18:07:49.769Z",
    "name": "tracks",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "lbjwgnwp",
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
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy");

  return dao.deleteCollection(collection);
})
