migrate((db) => {
  const collection = new Collection({
    "id": "5rip1ka0pg7s1ue",
    "created": "2023-10-20 21:08:34.604Z",
    "updated": "2023-10-20 21:08:34.604Z",
    "name": "saved",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "ofslynh4",
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
  const collection = dao.findCollectionByNameOrId("5rip1ka0pg7s1ue");

  return dao.deleteCollection(collection);
})
