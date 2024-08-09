migrate((db) => {
  const collection = new Collection({
    "id": "n5vopjvjg2w2p79",
    "created": "2023-10-20 21:08:54.190Z",
    "updated": "2023-10-20 21:08:54.190Z",
    "name": "tracks",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "3n1c8fnr",
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
  const collection = dao.findCollectionByNameOrId("n5vopjvjg2w2p79");

  return dao.deleteCollection(collection);
})
