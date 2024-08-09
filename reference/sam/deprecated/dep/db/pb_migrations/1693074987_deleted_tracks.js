migrate((db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("8lb1kv0zfo0i7xy");

  return dao.deleteCollection(collection);
}, (db) => {
  const collection = new Collection({
    "id": "8lb1kv0zfo0i7xy",
    "created": "2023-07-16 18:07:49.769Z",
    "updated": "2023-07-16 18:09:34.738Z",
    "name": "tracks",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "lbjwgnwp",
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
        "id": "sdih0v1r",
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
        "id": "avbeblgr",
        "name": "queue",
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
        "id": "hgduvins",
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
        "id": "dyancyx1",
        "name": "artists",
        "type": "json",
        "required": false,
        "unique": false,
        "options": {}
      },
      {
        "system": false,
        "id": "8acbept2",
        "name": "play_count",
        "type": "number",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null
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
