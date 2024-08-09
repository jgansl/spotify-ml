migrate((db) => {
  const collection = new Collection({
    "id": "5ypbx9bsf10v78z",
    "created": "2023-03-06 15:50:38.381Z",
    "updated": "2023-03-06 15:50:38.381Z",
    "name": "new_tracks",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "jagutirw",
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
  const collection = dao.findCollectionByNameOrId("5ypbx9bsf10v78z");

  return dao.deleteCollection(collection);
})
