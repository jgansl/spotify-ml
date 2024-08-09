migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("a75cw1kbc9cxewc");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "a75cw1kbc9cxewc",
    "created": "2023-12-04 23:57:27.898Z",
    "updated": "2023-12-05 23:47:05.455Z",
    "name": "heard",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "e7cpzx4s",
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
        "id": "tdvffckc",
        "name": "spotify_id",
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
        "id": "bdpfrksm",
        "name": "name",
        "type": "text",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
        "system": false,
        "id": "fejzr4ka",
        "name": "release_date",
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
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": "",
    "options": {}
  });

  return Dao(db).saveCollection(collection);
})
