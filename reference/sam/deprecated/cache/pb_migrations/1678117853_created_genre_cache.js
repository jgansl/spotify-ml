migrate((db) => {
  const collection = new Collection({
    "id": "p9blstqtrk7pmcl",
    "created": "2023-03-06 15:50:53.856Z",
    "updated": "2023-03-06 15:50:53.856Z",
    "name": "genre_cache",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "0rnln0m7",
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
  const collection = dao.findCollectionByNameOrId("p9blstqtrk7pmcl");

  return dao.deleteCollection(collection);
})
