migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("6ytsuxcbo48mqyf");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "6ytsuxcbo48mqyf",
    "created": "2023-06-08 20:20:52.263Z",
    "updated": "2023-07-25 14:39:48.462Z",
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
      },
      {
        "system": false,
        "id": "uvno08t5",
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
        "id": "afmmyeka",
        "name": "artists",
        "type": "json",
        "required": false,
        "unique": false,
        "options": {}
      },
      {
        "system": false,
        "id": "wej2t8w2",
        "name": "release_date",
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
        "id": "5ab3etzn",
        "name": "date_added",
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
