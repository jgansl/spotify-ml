migrate((db) => {
  const collection = new Collection({
    "id": "6sdrnap1eiw7h2i",
    "created": "2023-06-08 20:20:20.184Z",
    "updated": "2023-06-08 20:20:20.184Z",
    "name": "heard",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "zdc4xna6",
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
  const collection = dao.findCollectionByNameOrId("6sdrnap1eiw7h2i");

  return dao.deleteCollection(collection);
})
