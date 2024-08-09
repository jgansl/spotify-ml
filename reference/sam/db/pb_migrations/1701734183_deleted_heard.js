migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("ozirxi4mc7sfy1b");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "ozirxi4mc7sfy1b",
    "created": "2023-12-04 23:19:38.239Z",
    "updated": "2023-12-04 23:41:10.871Z",
    "name": "heard",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "qf2y4xpz",
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
        "id": "atq6zd5t",
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
        "id": "va69kohw",
        "name": "popularity",
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
        "id": "hkmcfltx",
        "name": "release_date",
        "type": "date",
        "required": false,
        "unique": false,
        "options": {
          "min": "",
          "max": ""
        }
      }
    ],
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
})
