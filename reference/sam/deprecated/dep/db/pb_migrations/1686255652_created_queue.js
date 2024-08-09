migrate((db) => {
  const collection = new Collection({
    "id": "6ytsuxcbo48mqyf",
    "created": "2023-06-08 20:20:52.263Z",
    "updated": "2023-06-08 20:20:52.263Z",
    "name": "queue",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "trank5bx",
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
        "id": "zcx9ux6r",
        "name": "queue_count",
        "type": "number",
        "required": false,
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
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf");

  return dao.deleteCollection(collection);
})
